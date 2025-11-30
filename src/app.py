import sys
from src.common.errors import SemanticError, TokenUnexpectedError
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

    try:
        source = read_source_code(source_path)
        dfa_rules = load_dfa_rules()
        lexer = Lexer(source, dfa_rules)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        parse_tree_root = parser.parse_program()
        
        if not parse_tree_root:
            return

        builder = ASTBuilder()
        ast_root = builder.build(parse_tree_root)

        analyzer = SemanticAnalyzer()
        analyzer.visit(ast_root)

        print("\nSemantic Analysis Successful.")
        
        print("\n===== SYMBOL TABLES =====")
        print_symbol_tables(analyzer.symtab)

        print("\n===== DECORATED AST =====")
        print_ast_tree(ast_root)

    except (SemanticError, TokenUnexpectedError) as e:
        print("\n" + "="*60)
        if isinstance(e, SemanticError):
            print(" COMPILATION FAILED: SEMANTIC ERROR")
        else:
            print(" COMPILATION FAILED: SYNTAX ERROR")
        print("="*60)
        
        line = getattr(e, 'line', None) or (e.token.line if hasattr(e, 'token') and e.token else None)
        col = getattr(e, 'column', None) or (e.token.column if hasattr(e, 'token') and e.token else None)
        
        if line and col:
            print(f" Location : Line {line}, Column {col}")
        
        msg = getattr(e, 'message', str(e))
        print(f" Message  : {msg}")
        print("="*60 + "\n")
        sys.exit(1)

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        sys.exit(1)