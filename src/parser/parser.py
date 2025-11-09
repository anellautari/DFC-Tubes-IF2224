from common.pascal_token import Token
from common.node import Node

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_index = 0
        self.errors = []

    def peek(self) -> Token | None:
        # lihat token saat ini tanpa mengonsumsi
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None
    
    def consume_token(self) -> Token | None:
        # ngambil token saat ini dan berpindah ke token berikutnya
        token = self.peek()
        if token:
            self.current_index += 1
        return token
    
    def match_token(self, expected_type: str, expected_value: str | None = None) -> Token | None:
        # mastiin token saat ini sesuai dengan yg diharapkan.
        # kalau ngga, muncul error syntax
        token = self.peek()
        if token is None:
            self.error(f"{expected_type}({expected_value})" if expected_value else expected_type, "EOF")
            return None
        
        if token.token_type == expected_type and (expected_value is None or token.value.lower() == expected_value.lower()):
            return self.consume_token()
        else:
            self.error(
                f"{expected_type}({expected_value})" if expected_value else expected_type,
                f"{token.token_type}({token.value})"
            )
            return None
        
    def error(self, expected: str, actual: str):
        # nampilin pesan error sintaks yg informatif
        msg = f"Syntax error: expected {expected}, but got {actual}"
        print(msg)
        self.errors.append(msg)       
        
    def parse_program(self):
        # Aturan grammar:
        # <program> ::= <program-header> <declaration-part> <compound-statement> DOT
        
        print("Memulai parsing program...")

        program_node = Node("<program>")

        program_header = self.parse_program_header()
        if program_header:
            program_node.add_children(program_header)

        decl_part = self.parse_declaration_part()
        if decl_part:
            program_node.add_children(decl_part)

        compound_stmt = self.parse_compound_statement()
        if compound_stmt:
            program_node.add_children(compound_stmt)

        dot_token = self.match_token("DOT", ".")
        if dot_token:
            program_node.add_children(Node("DOT", dot_token))
            
        program_node.print_tree()

        print("Selesai parsing program.")
        return program_node
        
    
    # === STUB FUNGSI GRAMMAR LEVEL 2 ===
    def parse_program_header(self):
        """
        <program-header> ::= 'program' <identifier> ';'
        """
        node = Node("<program-header>")
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "program")))
        node.add_children(Node("IDENTIFIER", self.match_token("IDENTIFIER")))
        node.add_children(Node("SEMICOLON", self.match_token("SEMICOLON", ";")))
        return node


    def parse_declaration_part(self):
        """
        <declaration-part> ::= { 'var' <var-declaration> ';' }
        (stub sederhana untuk menerima IDENTIFIER(var) + deklarasi dasar)
        """
        node = Node("<declaration-part>")

        tok = self.peek()
        # cuma deteksi "var" tanpa strict KEYWORD
        if tok and tok.value.lower() == "var":
            node.add_children(Node("IDENTIFIER", self.consume_token()))  # var
            # stub deklarasi satu variabel: x : integer;
            if self.peek() and self.peek().token_type == "IDENTIFIER":
                node.add_children(Node("IDENTIFIER", self.match_token("IDENTIFIER")))
            if self.peek() and self.peek().token_type == "COLON":
                node.add_children(Node("COLON", self.match_token("COLON", ":")))
            if self.peek() and self.peek().token_type in ("KEYWORD", "IDENTIFIER"):
                node.add_children(Node("TYPE", self.consume_token()))
            if self.peek() and self.peek().token_type == "SEMICOLON":
                node.add_children(Node("SEMICOLON", self.match_token("SEMICOLON", ";")))

        return node


    def parse_compound_statement(self):
        """
        <compound-statement> ::= 'begin' <statement-list> 'end'
        (stub versi sederhana, bisa baca satu assignment statement)
        """
        node = Node("<compound-statement>")
        
        # begin
        if self.peek() and self.peek().value.lower() == "begin":
            node.add_children(Node("IDENTIFIER", self.consume_token()))
        
        # satu statement: x := 10;
        if self.peek() and self.peek().token_type == "IDENTIFIER":
            assign_node = Node("<statement>")
            assign_node.add_children(Node("IDENTIFIER", self.match_token("IDENTIFIER")))
            if self.peek() and self.peek().token_type == "ASSIGN_OPERATOR":
                assign_node.add_children(Node("ASSIGN_OPERATOR", self.match_token("ASSIGN_OPERATOR", ":=")))
            if self.peek() and self.peek().token_type == "NUMBER":
                assign_node.add_children(Node("NUMBER", self.match_token("NUMBER")))
            if self.peek() and self.peek().token_type == "SEMICOLON":
                assign_node.add_children(Node("SEMICOLON", self.match_token("SEMICOLON", ";")))
            node.add_children(assign_node)

        # end
        if self.peek() and self.peek().value.lower() == "end":
            node.add_children(Node("IDENTIFIER", self.consume_token()))

        return node
