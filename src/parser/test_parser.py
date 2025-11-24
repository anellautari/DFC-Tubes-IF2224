# test_parser.py

from src.common.pascal_token import Token
from src.parser.parser import Parser

# Helper to make token quicker

def T(t, v, line=1, col=1):
    return Token(token_type=t, value=v, line=line, column=col)

# Sample token stream for simple program
sample_tokens = [
    T("KEYWORD", "program"),
    T("IDENTIFIER", "Basic"),
    T("SEMICOLON", ";"),

    T("IDENTIFIER", "var"),
    T("IDENTIFIER", "x"),
    T("COLON", ":"),
    T("KEYWORD", "integer"),
    T("SEMICOLON", ";"),

    T("IDENTIFIER", "mulai"),
    T("IDENTIFIER", "x"),
    T("ASSIGN_OPERATOR", ":="),
    T("NUMBER", "10"),
    T("SEMICOLON", ";"),
    T("IDENTIFIER", "selesai"),

    T("DOT", ".")
]


def run_test():
    parser = Parser(sample_tokens)
    ast = parser.parse_program()
    print("=== Parsing Done ===")

if __name__ == "__main__":
    run_test()
