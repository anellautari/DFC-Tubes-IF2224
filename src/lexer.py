from pascal_token import Token
from dfa import DFA

class Lexer:
    """
    Lexer: mengubah string kode sumber mentah menjadi daftar objek Token
    berdasarkan aturan yang didefinisikan dalam file DFA.
    """
    def __init__(self, source_code: str, dfa_rules: dict):
        """
        Inisialisasi lexer.
        
        Args:
            source_code (str): Seluruh kode sumber PASCAL-S sebagai satu string.
            dfa_rules (dict): Aturan DFA yang sudah di-load dari file JSON.
        """
        self.source_code = source_code
        self.dfa_rules = dfa_rules
        self.current_pos = 0
        self.current_line = 1
        self.current_col = 1
        
        self.keywords = set(dfa_rules.get("KEYWORDS", []))
        self.word_arithmetic = set(dfa_rules.get("WORD_ARITHMETIC", []))
        self.word_logical = set(dfa_rules.get("WORD_LOGICAL", []))

    def _get_next_token(self) -> Token | None:
        """
        Menganalisis kode sumber dari posisi saat ini untuk menemukan satu token berikutnya
        menggunakan aturan 'longest match'.
        """
        if self.current_pos >= len(self.source_code):
            return None  

        start_pos = self.current_pos
        start_line = self.current_line
        start_col = self.current_col

        last_final_state = None
        last_final_pos = -1
        
        current_state = self.dfa_rules["initial_state"]
        pos_tracker = self.current_pos

        while pos_tracker < len(self.source_code):
            char = self.source_code[pos_tracker]
            
            category = DFA.get_char_category(char)
            
            next_state = DFA.simulate_dfa_step(current_state, char, self.dfa_rules)

            if next_state is None:
                break
            
            current_state = next_state
            pos_tracker += 1

            if current_state in self.dfa_rules["final_states"]:
                last_final_state = current_state
                last_final_pos = pos_tracker

        if last_final_state is None:
            if not self.source_code[start_pos].isspace():
                self._handle_error(self.source_code[start_pos], start_line, start_col)
            
            self._advance_pos() 
            return None

        lexeme = self.source_code[start_pos:last_final_pos]
        
        self._set_pos_to(last_final_pos)
        
        return self._finalize_token(lexeme, last_final_state, start_line, start_col)

    def _finalize_token(self, lexeme: str, final_state: str, line: int, col: int) -> Token | None:
        """
        Membuat objek Token, melakukan lookup keyword, dan mengecek flag 'ignore'.
        """
        token_info = self.dfa_rules["final_states"][final_state]
        token_type = token_info["token"]

        if token_type == "IDENTIFIER":
            lexeme_lower = lexeme.lower()
            if lexeme_lower in self.keywords:
                token_type = "KEYWORD"
            elif lexeme_lower in self.word_arithmetic:
                token_type = "ARITHMETIC_OPERATOR"
            elif lexeme_lower in self.word_logical:
                token_type = "LOGICAL_OPERATOR"
        
        if token_type == "STRING_LITERAL":
            lexeme = lexeme.replace("''", "'")
        
        if token_info.get("ignore", False):
            return None  

        return Token(token_type=token_type, value=lexeme, line=line, column=col)

    def _handle_error(self, char: str, line: int, col: int):
        """
        Menangani error karakter tidak dikenal.
        """
        print(f"Error: Invalid character '{char}' at Line {line}:{col}")

    def _advance_pos(self):
        """Helper untuk memajukan lexer 1 karakter dan update line/col."""
        if self.current_pos >= len(self.source_code):
            return

        char = self.source_code[self.current_pos]
        if char == '\n':
            self.current_line += 1
            self.current_col = 1
        else:
            self.current_col += 1
        self.current_pos += 1

    def _set_pos_to(self, new_pos: int):
        """Helper untuk menggerakkan lexer ke posisi baru (setelah token) dan update line/col."""
        while self.current_pos < new_pos:
            self._advance_pos()

    def tokenize(self) -> list[Token]:
        """
        Fungsi publik utama untuk menjalankan keseluruhan proses tokenisasi. 
        """
        tokens = []
        while True:
            token = self._get_next_token()
            if token is None:
                if self.current_pos >= len(self.source_code):
                    break
                continue  
            
            tokens.append(token)
            
        return tokens