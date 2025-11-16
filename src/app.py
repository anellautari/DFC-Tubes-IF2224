import sys
from src.lexer.lexer import Lexer
from src.common.utils import load_dfa_rules, read_source_code
from src.parser.parser import Parser

def app():
    if len(sys.argv) != 2:
        print("Usage: python -m src.main <source_file.pas>")
        sys.exit(1)

    source_path = sys.argv[1]

    if source_path.endswith(".pas"):
        source = read_source_code(source_path)
        dfa_rules = load_dfa_rules()
        
        lexer = Lexer(source, dfa_rules)
        tokens = lexer.tokenize()
        
        for token in tokens:
           print(token)
        
        parser = Parser(tokens)
        parser.parse_program()

    else:
        print("Error: Input file harus berekstensi .pas")
        sys.exit(1)