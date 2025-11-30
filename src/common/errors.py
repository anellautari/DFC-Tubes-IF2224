class CompilerError(Exception):
    """Base class for compiler-related errors."""


class LexicalError(CompilerError):
    def __init__(self, message: str, line: int | None = None, column: int | None = None):
        if line is not None and column is not None:
            super().__init__(f"[LexicalError] {message} @ {line}:{column}")
        else:
            super().__init__(f"[LexicalError] {message}")


class SyntaxParseError(CompilerError):
    def __init__(self, message: str, line: int | None = None, column: int | None = None):
        if line is not None and column is not None:
            super().__init__(f"[SyntaxParseError] {message} @ {line}:{column}")
        else:
            super().__init__(f"[SyntaxParseError] {message}")


class TokenUnexpectedError(SyntaxParseError):
    def __init__(self, expected: str, actual: str, line: int | None = None, column: int | None = None):
        msg = f"Expected {expected}, but got {actual}"
        super().__init__(msg, line, column)


class SemanticError(CompilerError):
    def __init__(self, message: str):
        super().__init__(f"[SemanticError] {message}")
