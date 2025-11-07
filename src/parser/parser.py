from common.pascal_token import Token

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_index = 0
        self.errors = []

    def peek(self) -> Token | None:
        # lihat token saat ini tanpa mengonsumsi
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None
    
    def consume_token(self) -> Token | None:
        # ngambil token saat ini dan berpindah ke token berikutnya
        token = self.peek()
        if token:
            self.current_index += 1
        return token
    
    def match_token(self, expected_type: str, expected_value: str | None = None) -> Token | None:
        # mastiin token saat ini sesuai dengan yg diharapkan.
        # kalau ngga, muncul error syntax
        token = self.peek()
        if token is None:
            self.error(f"{expected_type}({expected_value})" if expected_value else expected_type, "EOF")
            return None
        
        if token.token_type == expected_type and (expected_value is None or token.value.lower() == expected_value.lower()):
            return self.consume_token()
        else:
            self.error(
                f"{expected_type}({expected_value})" if expected_value else expected_type,
                f"{token.token_type}({token.value})"
            )
            return None
        
    def error(self, expected: str, actual: str):
        # nampilin pesan error sintaks yg informatif
        msg = f"Syntax error: expected {expected}, but got {actual}"
        print(msg)
        self.errors.append(msg)


    # STUB FUNGSI GRAMMAR LEVEL ATAS
    def parse_program(self):
        # Aturan grammar:
        # <program> ::= <program-header> <declaration-part> <compound-statement> DOT

        # fungsi sementara, cuma ngecek validasi token pertama (nanti sesuaikan saja)
        print("Memulai parsing program...")
        token = self.match_token("KEYWORD", "program")
        if token:
            ident = self.match_token("IDENTIFIER")
            self.match_token("SEMICOLON")
        print("Selesai parse_program sementara")        