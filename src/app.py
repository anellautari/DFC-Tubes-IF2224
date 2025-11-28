import sys
from src.lexer.lexer import Lexer
from src.common.utils import load_dfa_rules, read_source_code, print_symbol_tables, print_ast_tree
from src.parser.parser import Parser
from src.semantic.ast_builder import ASTBuilder
from src.semantic.semantic_analyzer import SemanticAnalyzer

def app():
    if len(sys.argv) != 2:
        print("Usage: python -m src.main <source_file.pas>")
        sys.exit(1)

    source_path = sys.argv[1]

    if not source_path.endswith(".pas"):
        print("Error: Input file harus berekstensi .pas")
        sys.exit(1)

    source = read_source_code(source_path)
    dfa_rules = load_dfa_rules()
    lexer = Lexer(source, dfa_rules)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    parse_tree_root = parser.parse_program()

    builder = ASTBuilder()
    ast_root = builder.build(parse_tree_root)

    analyzer = SemanticAnalyzer()
    analyzer.visit(ast_root)

    print("\n===== SYMBOL TABLES =====")
    print_symbol_tables(analyzer.symtab)

    print("\n===== DECORATED AST =====")
    print_ast_tree(ast_root)

