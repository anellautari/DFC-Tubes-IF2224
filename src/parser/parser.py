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
        # nampilin pesan error sintaks
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
    
    def parse_block(self):
        """<block> ::= <declaration-part> <compound-statement>

        Dipakai oleh deklarasi procedure / function.
        """
        node = Node("<block>")
        decl = self.parse_declaration_part()
        if decl:
            node.add_children(decl)
        comp = self.parse_compound_statement()
        if comp:
            node.add_children(comp)
        return node
    
    def parse_declaration_part(self):
        """<declaration-part> ::=
            { <const-declaration> }
            { <type-declaration> }
            { <var-declaration> }
            { <subprogram-declaration> }
        """
        node = Node("<declaration-part>")

        while True:
            tok = self.peek()
            if not tok or tok.token_type != "KEYWORD":
                break

            kw = tok.value.lower()

            if kw == "konstanta":
                const_node = self.parse_const_declaration()
                if const_node:
                    node.add_children(const_node)
                continue

            if kw == "tipe":
                type_decl = self.parse_type_declaration()
                if type_decl:
                    node.add_children(type_decl)
                continue

            if kw == "variabel":
                var_decl = self.parse_var_declaration()
                if var_decl:
                    node.add_children(var_decl)
                continue

            if kw in ("prosedur", "fungsi"):
                subprog = self.parse_subprogram_declaration()
                if subprog:
                    node.add_children(subprog)
                continue

            break

        return node if node.children else None
    
    # ====== CONST DECLARATION ======
    def parse_const_declaration(self):
        """<const-declaration> ::= 'konstanta' ( IDENTIFIER '=' <expression> ';' )+"""
        node = Node("<const-declaration>")
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "konstanta")))

        # Minimal satu definisi konstanta
        while True:
            ident = self.match_token("IDENTIFIER")
            if not ident:
                break
            node.add_children(Node("IDENTIFIER", ident))

            eq = self.match_token("RELATIONAL_OPERATOR", "=")
            if not eq:
                break
            node.add_children(Node("RELATIONAL_OPERATOR", eq))

            value_expr = self.parse_expression()
            if value_expr:
                node.add_children(value_expr)
            else:
                # fallback sederhana: kalau parse_expression belum diisi,
                # setidaknya konsumsi literal / identifier.
                lit = self.peek()
                if lit and lit.token_type in ("NUMBER", "CHAR_LITERAL", "STRING_LITERAL", "IDENTIFIER"):
                    node.add_children(Node(lit.token_type, self.consume_token()))
                else:
                    break

            semi = self.match_token("SEMICOLON", ";")
            if not semi:
                break
            node.add_children(Node("SEMICOLON", semi))

            # cek apakah masih ada IDENTIFIER lagi (definisi konstanta berikutnya)
            nxt = self.peek()
            if not (nxt and nxt.token_type == "IDENTIFIER"):
                break

        return node

    # ====== TYPE DECLARATION ======
    def parse_type_declaration(self):
        """<type-declaration> ::= 'tipe' ( IDENTIFIER '=' <type> ';' )+"""
        node = Node("<type-declaration>")
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "tipe")))

        while True:
            ident = self.match_token("IDENTIFIER")
            if not ident:
                break
            node.add_children(Node("IDENTIFIER", ident))

            eq = self.match_token("RELATIONAL_OPERATOR", "=")
            if not eq:
                break
            node.add_children(Node("RELATIONAL_OPERATOR", eq))

            type_node = self.parse_type()
            if type_node:
                node.add_children(type_node)

            semi = self.match_token("SEMICOLON", ";")
            if not semi:
                break
            node.add_children(Node("SEMICOLON", semi))

            nxt = self.peek()
            if not (nxt and nxt.token_type == "IDENTIFIER"):
                break

        return node

    def parse_type(self):
        """<type> ::= 'integer' | 'real' | 'boolean' | 'char' | <array-type>"""
        node = Node("<type>")
        tok = self.peek()

        if tok and tok.token_type == "KEYWORD":
            kw = tok.value.lower()
            if kw in ("integer", "real", "boolean", "char"):
                node.add_children(Node("KEYWORD", self.consume_token()))
                return node
            if kw == "larik":
                array_node = self.parse_array_type()
                if array_node:
                    node.add_children(array_node)
                return node

        # kalau tidak cocok grammar, catat error tapi tetap coba lanjut
        if tok:
            self.error("type", f"{tok.token_type}({tok.value})")
            node.add_children(Node(tok.token_type, self.consume_token()))
            return node

        self.error("type", "EOF")
        return node

    def parse_array_type(self):
        """<array-type> ::= 'larik' '[' <range> ']' 'dari' <type>"""
        node = Node("<array-type>")

        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "larik")))
        node.add_children(Node("LBRACKET", self.match_token("LBRACKET", "[")))

        range_node = self.parse_range()
        if range_node:
            node.add_children(range_node)

        node.add_children(Node("RBRACKET", self.match_token("RBRACKET", "]")))
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "dari")))

        elem_type = self.parse_type()
        if elem_type:
            node.add_children(elem_type)

        return node

    def parse_range(self):
        """<range> ::= <expression> RANGE_OPERATOR <expression>"""
        node = Node("<range>")

        left = self.parse_expression()
        if left:
            node.add_children(left)

        node.add_children(Node("RANGE_OPERATOR", self.match_token("RANGE_OPERATOR", "..")))

        right = self.parse_expression()
        if right:
            node.add_children(right)

        return node
    
    # ====== VAR DECLARATION ======
    def parse_var_declaration(self):
        """<var-declaration> ::= 'variabel' ( <identifier-list> ':' <type> ';' )+"""
        node = Node("<var-declaration>")
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "variabel")))

        while True:
            ident_list = self.parse_identifier_list()
            if not ident_list:
                break
            node.add_children(ident_list)

            node.add_children(Node("COLON", self.match_token("COLON", ":")))

            type_node = self.parse_type()
            if type_node:
                node.add_children(type_node)

            semi = self.match_token("SEMICOLON", ";")
            if not semi:
                break
            node.add_children(Node("SEMICOLON", semi))

            nxt = self.peek()
            # kalau setelah ';' masih IDENTIFIER, berarti masih dalam blok var yang sama
            if not (nxt and nxt.token_type == "IDENTIFIER"):
                break

        return node
    
    def parse_identifier_list(self):
        """<identifier-list> ::= IDENTIFIER (',' IDENTIFIER)*"""
        node = Node("<identifier-list>")

        first = self.match_token("IDENTIFIER")
        if not first:
            return None
        node.add_children(Node("IDENTIFIER", first))

        while self.peek() and self.peek().token_type == "COMMA":
            comma_tok = self.consume_token()
            node.add_children(Node("COMMA", comma_tok))

            ident = self.match_token("IDENTIFIER")
            if not ident:
                break
            node.add_children(Node("IDENTIFIER", ident))

        return node
    
    # ====== SUBPROGRAM DECLARATION ======
    def parse_subprogram_declaration(self):
        """<subprogram-declaration> ::= <procedure-declaration> | <function-declaration>"""
        tok = self.peek()
        if not tok or tok.token_type != "KEYWORD":
            return None

        if tok.value.lower() == "prosedur":
            return self.parse_procedure_declaration()
        if tok.value.lower() == "fungsi":
            return self.parse_function_declaration()
        return None

    def parse_procedure_declaration(self):
        """<procedure-declaration> ::
            'prosedur' IDENTIFIER [ <formal-parameter-list> ] ';' <block> ';'
        """
        node = Node("<procedure-declaration>")

        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "prosedur")))
        node.add_children(Node("IDENTIFIER", self.match_token("IDENTIFIER")))

        # [ formal-parameter-list ]
        if self.peek() and self.peek().token_type == "LPARENTHESIS":
            fp = self.parse_formal_parameter_list()
            if fp:
                node.add_children(fp)

        node.add_children(Node("SEMICOLON", self.match_token("SEMICOLON", ";")))

        block = self.parse_block()
        if block:
            node.add_children(block)

        node.add_children(Node("SEMICOLON", self.match_token("SEMICOLON", ";")))

        return node

    def parse_function_declaration(self):
        """<function-declaration> ::
            'fungsi' IDENTIFIER [ <formal-parameter-list> ] ':' <type> ';' <block> ';'
        """
        node = Node("<function-declaration>")

        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "fungsi")))
        node.add_children(Node("IDENTIFIER", self.match_token("IDENTIFIER")))

        if self.peek() and self.peek().token_type == "LPARENTHESIS":
            fp = self.parse_formal_parameter_list()
            if fp:
                node.add_children(fp)

        node.add_children(Node("COLON", self.match_token("COLON", ":")))

        ret_type = self.parse_type()
        if ret_type:
            node.add_children(ret_type)

        node.add_children(Node("SEMICOLON", self.match_token("SEMICOLON", ";")))

        block = self.parse_block()
        if block:
            node.add_children(block)

        node.add_children(Node("SEMICOLON", self.match_token("SEMICOLON", ";")))

        return node

    def parse_formal_parameter_list(self):
        """<formal-parameter-list> ::=
            '(' <parameter-group> ( ';' <parameter-group> )* ')'
        """
        node = Node("<formal-parameter-list>")

        node.add_children(Node("LPARENTHESIS", self.match_token("LPARENTHESIS", "(")))

        param_group = self.parse_parameter_group()
        if param_group:
            node.add_children(param_group)

        while self.peek() and self.peek().token_type == "SEMICOLON":
            semi = self.consume_token()
            node.add_children(Node("SEMICOLON", semi))

            param_group = self.parse_parameter_group()
            if not param_group:
                break
            node.add_children(param_group)

        node.add_children(Node("RPARENTHESIS", self.match_token("RPARENTHESIS", ")")))
        return node

    def parse_parameter_group(self):
        """<parameter-group> ::= <identifier-list> ':' <type>"""
        node = Node("<parameter-group>")

        ident_list = self.parse_identifier_list()
        if not ident_list:
            return None
        node.add_children(ident_list)

        node.add_children(Node("COLON", self.match_token("COLON", ":")))

        type_node = self.parse_type()
        if type_node:
            node.add_children(type_node)

        return node
    
    # ====== COMPOUND STATEMENT ======
    def parse_statement(self):
        nextToken = self.peek()
        if not nextToken:
            self.error("EOF")
        if nextToken.value == "jika":
            return self.parse_if_statement()
        elif nextToken.value == "selama":
            return self.parse_while_statement()
        elif nextToken.value == "untuk":
            return self.parse_for_statement()
        elif nextToken.token_type == "IDENTIFIER":
            return self.parse_assignment_statement()
        elif nextToken.value == "mulai":
            return self.parse_compound_statement()
        else:
            self.error("Unexpected token in statement")
        
    def parse_if_statement(self):
        # <if-statement> ::= 'if' <expression> 'then' <statement> [ 'else' <statement> ]

        node = Node("<if-statement>")
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "if")))

        node.add_children(self.parse_expression())

        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "then")))
        node.add_children(self.parse_statement())

        token = self.peek()
        if token and token.value == "else":
            node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "else")))
            node.add_children(self.parse_statement())

        return node

    def parse_while_statement(self):
        # <while-statement> ::= 'while' <expression> 'do' <statement>

        node = Node("<while-statement>")
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "while")))
        
        node.add_children(self.parse_expression())

        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "do")))
        node.add_children(self.parse_statement())

        return node
    
    def parse_for_statement(self):
        # <for-statement> ::= 'for' <identifier> ':=' <expression> 'to' <expression> 'do' <statement>
        
        node = Node("<for-statement>")
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "for")))
        node.add_children(Node("IDENTIFIER", self.match_token("IDENTIFIER")))
        node.add_children(Node("ASSIGN_OPERATOR", self.match_token("ASSIGN_OPERATOR", ":=")))
        node.add_children(self.parse_expression())
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "to")))
        node.add_children(self.parse_expression())
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "do")))
        node.add_children(self.parse_statement())

        return node
    
    def parse_assignment_statement(self):
        # <assignment-statement> ::= <identifier> ':=' <expression>
        
        node = Node("<assignment-statement>")
        node.add_children(Node("IDENTIFIER", self.match_token("IDENTIFIER")))
        node.add_children(Node("ASSIGN_OPERATOR", self.match_token("ASSIGN_OPERATOR", ":=")))
        node.add_children(self.parse_expression())

        return node

    def parse_compound_statement(self):
        """
        <compound-statement> ::= 'begin' <statement-list> 'end'
        """
        node = Node("<compound-statement>")
        
        # begin
        if self.peek() and self.peek().value.lower() == "mulai":
            node.add_children(Node("IDENTIFIER", self.consume_token()))
            while self.peek() and self.peek().value.lower() != "selesai" :
                statement_node = self.parse_statement()
                if statement_node:
                    node.add_children(statement_node)
            node.add_children(Node("IDENTIFIER", self.consume_token()))
            
        else:
            self.error("IDENTIFIER(mulai)", "EOF" if self.peek() is None else f"{self.peek().token_type}({self.peek().value})")


        return node
    
    def parse_assignment_statement(self):
        # <assignment-statement> ::= IDENTIFIER ASSIGN_OPERATOR <expression>
        node = Node("<assignment-statement>")
        
        # IDENTIFIER
        ident = self.match_token("IDENTIFIER")
        if not ident: return None
        node.add_children(Node("IDENTIFIER", ident))
        
        # ASSIGN_OPERATOR
        op = self.match_token("ASSIGN_OPERATOR", ":=")
        if not op: return None
        node.add_children(Node("ASSIGN_OPERATOR", op))
        
        expr_node = self.parse_expression()
        if not expr_node:
            self.error("expression", self.peek().token_type if self.peek() else "EOF")
            return None
        node.add_children(expr_node)
        
        return node

    def parse_procedure_call(self):
        # <procedure-call> ::= IDENTIFIER [ LPARENTHESIS <parameter-list> RPARENTHESIS ]
        node = Node("<procedure-function-call>")
        
        # IDENTIFIER
        ident = self.match_token("IDENTIFIER")
        if not ident: return None
        node.add_children(Node("IDENTIFIER", ident))
        
        # [ ... ] 
        if self.peek() and self.peek().token_type == "LPARENTHESIS":
            lparen = self.consume_token() 
            node.add_children(Node("LPARENTHESIS", lparen))
            
            param_list_node = self.parse_parameter_list()
            if param_list_node:
                node.add_children(param_list_node)
            
            rparen = self.match_token("RPARENTHESIS", ")")
            if not rparen: return None
            node.add_children(Node("RPARENTHESIS", rparen))
            
        return node

    def parse_function_call(self):
        # <function-call> ::= IDENTIFIER LPARENTHESIS [ <parameter-list> ] RPARENTHESIS
        node = Node("<function-call>")
        
        # IDENTIFIER
        ident = self.match_token("IDENTIFIER")
        if not ident: return None
        node.add_children(Node("IDENTIFIER", ident))
        
        # LPARENTHESIS
        lparen = self.match_token("LPARENTHESIS", "(")
        if not lparen: return None
        node.add_children(Node("LPARENTHESIS", lparen))
        
        if self.peek() and self.peek().token_type != "RPARENTHESIS":
            param_list_node = self.parse_parameter_list()
            if param_list_node:
                node.add_children(param_list_node)
        
        # RPARENTHESIS
        rparen = self.match_token("RPARENTHESIS", ")")
        if not rparen: return None
        node.add_children(Node("RPARENTHESIS", rparen))
        
        return node
    
    def parse_parameter_list(self):
        # <parameter-list> ::= <expression> { COMMA <expression> }
        node = Node("<parameter-list>")
        
        # <expression> pertama
        expr_node = self.parse_expression()
        if not expr_node:
            # List parameter boleh kosong (misal: writeln())
            return None 
        
        node.add_children(expr_node)
        
        # { COMMA <expression> }
        while self.peek() and self.peek().token_type == "COMMA":
            comma_node = Node("COMMA", self.consume_token())
            node.add_children(comma_node)
            
            expr_node = self.parse_expression()
            if not expr_node:
                self.error("expression", self.peek().token_type if self.peek() else "EOF")
                return None # Error, koma harus diikuti ekspresi
            node.add_children(expr_node)
            
        return node

    def parse_expression(self):
        pass
    
    def parse_simple_expression(self):
        pass