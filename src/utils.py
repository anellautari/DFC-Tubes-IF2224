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
    else: 
        return None

def process_input_with_dfa(text: str, dfa_rules: dict) -> None:
    """
    Mensimulasikan proses DFA terhadap seluruh input string.

    Fungsi ini tidak melakukan tokenisasi, hanya menunjukkan urutan
    transisi state untuk debugging atau verifikasi DFA.

    Args:
        text (str): String input yang akan diuji (misal satu baris kode Pascal).
        dfa_rules (dict): Aturan DFA yang sudah dimuat dari JSON.
    """
    current_state = dfa_rules["initial_state"]
    final_states = dfa_rules["final_states"]

    print(f"Start state: {current_state}")

    for i, char in enumerate(text):
        next_state = simulate_dfa_step(current_state, char, dfa_rules)
        category = get_char_category(char)
        if next_state is None:
            print(f"Error: Tidak ada transisi dari state '{current_state}' dengan input '{char}' (kategori: {category})")
            break
        print(f"[{i}] '{char}' ({category}) -> {next_state}")
        current_state = next_state

    if current_state in final_states:
        token_type = final_states[current_state]
        print(f"Input diterima. Berhenti di final state '{current_state}' dengan token type: {token_type}")
    else:
        print(f"Input tidak diterima. Berhenti di state '{current_state}'")