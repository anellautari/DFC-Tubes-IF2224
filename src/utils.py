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
