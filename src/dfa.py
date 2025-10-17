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

        if char in current_transitions:
            return current_transitions[char]
         
        category = DFA.get_char_category(char)

        if category in current_transitions:
            return current_transitions[category]
        elif "ANY" in current_transitions:
            return current_transitions["ANY"]
        else: 
            return None
