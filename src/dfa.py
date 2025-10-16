class DFA:
    @staticmethod
    def get_char_category(char: str) -> str:
        """
        Mengklasifikasikan sebuah karakter ke dalam kategori yang dikenali oleh DFA.
        
        Fungsi ini bertindak sebagai pemetaan dari karakter spesifik ('a', 'b', '7', ';') 
        ke kategori umum yang ada di file dfa_rules.json.
        
        Args:
            char (str): Karakter tunggal yang akan diklasifikasikan.
            
        Returns:
            str: Nama kategori yang sesuai (misal: 'LETTER', 'DIGIT', 'WHITESPACE').
        """
        if char.isalpha():
            return "LETTER"
        elif char.isdigit():
            return "DIGIT"
        elif char == '\n' or char == '\r':
            return "NEWLINE"
        elif char.isspace():
            return "WHITESPACE"
        elif char == '_':
            return "UNDERSCORE"
        elif char in ['+', '-', '*', '/', '=', '<', '>', ':', ';',
                    ',', '.','(', ')', '{', '}', '[', ']', '\'']:
            return char
        else:
            return "UNKNOWN"

    @staticmethod
    def simulate_dfa_step(current_state: str, char: str, dfa_rules: dict) -> str:
        """
        Melakukan satu langkah transisi DFA berdasarkan karakter input.

        Args:
            current_state (str): State saat ini.
            char (str): Karakter input tunggal yang dibaca.
            dfa_rules (dict): Aturan DFA yang berisi 'transitions', 'initial_state', dan 'final_states'.

        Returns:
            str: State berikutnya setelah membaca karakter tersebut.
                Jika tidak ada transisi yang valid, mengembalikan None.
        """
        transitions = dfa_rules.get("transitions", {})
        current_transitions = transitions.get(current_state, {})

        category = DFA.get_char_category(char)

        if category in current_transitions:
            return current_transitions[category]
        elif char in current_transitions:
            return current_transitions[char]
        elif "ANY" in current_transitions:
            return current_transitions["ANY"]
        else: 
            return None

    @staticmethod
    def scan_tokens(text: str, dfa_rules: dict) -> list:
        """
        Memproses input string dan mengembalikan daftar lexeme beserta final state-nya.
        Menghasilkan list of token dengan format:
        [{'lexeme': 'program', 'final_state': 'IDENTIFIER'}, ...]
        """
        tokens = []
        start_state = dfa_rules["initial_state"]
        final_states = dfa_rules["final_states"]

        current_state = start_state
        current_lexeme = ""

        i = 0
        while i < len(text):
            ch = text[i]
            category = DFA.get_char_category(ch)

            # spasi/tab di awal -> skip
            if current_state == start_state and category in ["WHITESPACE", "NEWLINE"]:
                i += 1
                continue

            next_state = DFA.simulate_dfa_step(current_state, ch, dfa_rules)

            if next_state is not None:
                current_lexeme += ch
                current_state = next_state
                i += 1
                continue

            # kalau current = final -> emit token
            if current_state in final_states and current_lexeme:
                token_info = final_states[current_state]
                tokens.append({
                    "lexeme": current_lexeme,
                    "final_state": current_state
                })
                current_state = start_state
                current_lexeme = ""
                continue

            # kalau char = whitespace -> reset
            if category in ["WHITESPACE", "NEWLINE"]:
                # reset
                current_state = start_state
                current_lexeme = ""
                i += 1
                continue

            single_state = DFA.simulate_dfa_step(start_state, ch, dfa_rules)
            if single_state is not None and single_state in final_states:
                token_info = final_states[single_state]
                tokens.append({
                    "lexeme": ch,
                    "final_state": single_state
                })
                i += 1
                current_state = start_state
                current_lexeme = ""
                continue

            i += 1

        # token teralhir
        if current_state in final_states and current_lexeme:
            tokens.append({
                "lexeme": current_lexeme,
                "final_state": current_state
            })

        return tokens