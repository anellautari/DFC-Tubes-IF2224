import sys
from src.lexer.lexer import Lexer
from src.common.utils import load_dfa_rules, read_source_code, load_tokens_from_file

def app():
    # input .pas: Menjalankan Lexer -> Parser (pake list token dari memory)
    # input .txt: Menjalankan Parser (pake list token dari file .txt)

    # Validasi input dari command line
    if len(sys.argv) != 2:
        print("Usage: python -m src.main <source_file.pas | token_file.txt>")
        sys.exit(1)

    source_path = sys.argv[1]
    tokens = []

    if source_path.endswith(".pas"):
        # Input adalah source code .pas -> jalanin lexer untuk mendapatkan list[Token] in-memory
        
        dfa_path = "src/dfa_rules.json"
        source = read_source_code(source_path)
        dfa_rules = load_dfa_rules(dfa_path)
        
        lexer = Lexer(source, dfa_rules)
        tokens = lexer.tokenize()
        
        for token in tokens:
           print(token)

    elif source_path.endswith(".txt"):
        # Input adalah file token .txt -> baca file .txt dan mem-parsing-nya menjadi list[Token]
        
        tokens = load_tokens_from_file(source_path)
        
        for token in tokens:
           print(token)

    else:
        print("Error: Input file harus berekstensi .pas atau .txt")
        sys.exit(1)
