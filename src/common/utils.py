import os
import json
import sys
import re
from src.common.pascal_token import Token

def load_dfa_rules(filepath: str | None = None) -> dict:
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
    if filepath is None:
        current_dir = os.path.dirname(__file__) 
        project_root = os.path.dirname(current_dir)
        filepath = os.path.join(project_root, "lexer", "dfa_rules.json")

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
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
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File source code '{path}' tidak ditemukan.")
        sys.exit(1)
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file source code '{path}': {e}")
        sys.exit(1)