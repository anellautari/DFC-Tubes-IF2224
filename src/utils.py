import json
import sys

def load_dfa_rules(filepath: str) -> dict:
    """
    Membaca file aturan DFA dalam format JSON dan mengubahnya menjadi dictionary.
    
    Fungsi ini menangani pembukaan file dan parsing JSON. Jika terjadi error,
    seperti file tidak ditemukan atau format JSON tidak valid, fungsi akan
    mencetak pesan error dan menghentikan program secara aman.
    
    Args:
        filepath (str): Path menuju file dfa_rules.json.
        
    Returns:
        dict: Dictionary yang berisi aturan transisi, state awal, dan final states.
              Mengembalikan None jika terjadi error.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            dfa_rules = json.load(file)
            return dfa_rules
    except FileNotFoundError:
        print(f"Error: File '{filepath}' tidak ditemukan.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: File '{filepath}' bukan file JSON valid: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file DFA '{filepath}': {e}")
        sys.exit(1)

def read_source_code(path):
    """
    Membaca file Pascal-S input dan mengembalikan string kontennya.
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_char_category(char: str) -> str:
    """
    Mengklasifikasikan sebuah karakter ke dalam kategori yang dikenali oleh DFA.
    
    Aturan DFA kita di `dfa_rules.json` menggunakan kategori umum seperti 'LETTER'
    atau 'DIGIT' daripada setiap karakter individual. Fungsi ini bertindak
    sebagai pemetaan dari karakter spesifik ('a', 'b', '7', ';') ke kategori
    umumnya.
    
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

    from utils import get_char_category
    category = get_char_category(char)

    if category in current_transitions:
        return current_transitions[category]
    elif char in current_transitions:
        return current_transitions[char]
    elif "ANY" in current_transitions:
        return current_transitions["ANY"]
    else: 
        return None

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
        category = get_char_category(ch)

        # spasi/tab di awal -> skip
        if current_state == start_state and category in ["WHITESPACE", "NEWLINE"]:
            i += 1
            continue

        next_state = simulate_dfa_step(current_state, ch, dfa_rules)

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

        single_state = simulate_dfa_step(start_state, ch, dfa_rules)
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