import json

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
    pass

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
    pass