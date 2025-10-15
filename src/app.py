import sys
# from .lexer import Lexer
from utils import load_dfa_rules, read_source_code, scan_tokens

def app():
    """
    Fungsi utama yang mengorkestrasi seluruh alur kerja program.
    
    Tugasnya meliputi:
    1. Memvalidasi argumen command-line.
    2. Membaca file input kode sumber `.pas`.
    3. Memuat aturan DFA dari file JSON menggunakan fungsi dari utils.
    4. Membuat instance dari kelas Lexer.
    5. Menjalankan proses tokenisasi.
    6. Mencetak hasilnya ke konsol dengan format yang sesuai.
    """

    # Langkah 1: Validasi input dari command line
    if len(sys.argv) != 2:
        print("Usage: python app.py <source_file.pas>")
        sys.exit(1)

    source_path = sys.argv[1]
    dfa_path = "dfa_rules.json"

    # Langkah 2: Baca konten file source code
    source = read_source_code(source_path)
    
    # Langkah 3: Muat aturan DFA
    dfa_rules = load_dfa_rules(dfa_path)
    lines = source.splitlines()

    for i, line in enumerate(lines, start=1):
        tokens = scan_tokens(line, dfa_rules)
        # DEBUG (nanti janlup hapus)
        print(f"Line {i} tokens: {tokens}\n")

    # Langkah 4: Buat objek Lexer dan jalankan tokenisasi
    pass

    # Langkah 5: Cetak setiap token dalam daftar hasil
    pass