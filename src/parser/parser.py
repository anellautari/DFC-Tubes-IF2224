import logging
from src.common.pascal_token import Token
from src.common.node import Node
from src.common.errors import TokenUnexpectedError

class Parser:
    def __init__(self, tokens: list[Token], raise_on_error: bool = False):
        self.tokens = tokens
        self.current_index = 0
        self.errors = []
        self.raise_on_error = raise_on_error

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
            self.error(f"{expected_type}({expected_value})" if expected_value else expected_type, None)
            return None
        
        if token.token_type == expected_type and (expected_value is None or token.value.lower() == expected_value.lower()):
            return self.consume_token()
        else:
            self.error(
                f"{expected_type}({expected_value})" if expected_value else expected_type,
                token
            )
            return None
        
    def error(self, expected: str, actual_token: Token | None):
        actual_desc = self._fmt_token(actual_token)
        line, col = (actual_token.line, actual_token.column) if actual_token else (None, None)
        msg = f"Syntax error: expected {expected}, but got {actual_desc}"
        logging.error(msg)
        self.errors.append(msg)
        if self.raise_on_error:
            raise TokenUnexpectedError(expected, actual_desc, line, col)

    def _fmt_token(self, tok: Token | None) -> str:
        if tok is None:
            return "EOF"
        return f"{tok.token_type}({tok.value}) @ {tok.line}:{tok.column}"
        
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
            self.error("type", tok)
            node.add_children(Node(tok.token_type, self.consume_token()))
            return node

        self.error("type", None)
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

        while True:
            tok = self.peek()
            if not tok or tok.token_type != "COMMA":
                break
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
        tok = self.peek()
        if tok and tok.token_type == "LPARENTHESIS":
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

        tok = self.peek()
        if tok and tok.token_type == "LPARENTHESIS":
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

        while True:
            tok = self.peek()
            if not tok or tok.token_type != "SEMICOLON":
                break
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
        tok = self.peek()
        if not tok:
            self.error("statement", None)
            return None
        if tok.token_type == "KEYWORD":
            kw = tok.value.lower()
            if kw == "jika":
                return self.parse_if_statement()
            elif kw == "selama":
                return self.parse_while_statement()
            elif kw == "untuk":
                return self.parse_for_statement()
            elif kw == "mulai":
                return self.parse_compound_statement()
        if tok.token_type == "IDENTIFIER":
            return self.parse_assignment_statement()
        self.error("statement", tok)
        return None
        
    def parse_if_statement(self):
        # <if-statement> ::= 'if' <expression> 'then' <statement> [ 'else' <statement> ]

        node = Node("<if-statement>")
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "jika")))

        node.add_children(self.parse_expression())

        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "maka")))
        node.add_children(self.parse_statement())

        token = self.peek()
        if token and token.token_type == "KEYWORD" and token.value.lower() in ("selain_itu"):
            node.add_children(Node("KEYWORD", self.consume_token()))
            node.add_children(self.parse_statement())

        return node

    def parse_while_statement(self):
        # <while-statement> ::= 'while' <expression> 'do' <statement>

        node = Node("<while-statement>")
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "selama")))
        
        node.add_children(self.parse_expression())

        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "lakukan")))
        node.add_children(self.parse_statement())

        return node
    
    def parse_for_statement(self):
        # <for-statement> ::= 'untuk' IDENTIFIER ':=' <expression> ('ke'|'turun_ke') <expression> 'lakukan' <statement>
        
        node = Node("<for-statement>")
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "untuk")))
        node.add_children(Node("IDENTIFIER", self.match_token("IDENTIFIER")))
        node.add_children(Node("ASSIGN_OPERATOR", self.match_token("ASSIGN_OPERATOR", ":=")))
        node.add_children(self.parse_expression())
        dir_tok = self.peek()
        if dir_tok and dir_tok.token_type == "KEYWORD" and dir_tok.value.lower() in ("ke", "turun_ke", "turun-ke"):
            node.add_children(Node("KEYWORD", self.consume_token()))
        else:
            self.error("KEYWORD(ke|turun_ke)", dir_tok)
        node.add_children(self.parse_expression())
        node.add_children(Node("KEYWORD", self.match_token("KEYWORD", "lakukan")))
        node.add_children(self.parse_statement())

        return node
    
    # remove duplicate earlier variant of parse_assignment_statement (kept the robust version below)

    def parse_compound_statement(self):
        """
        <compound-statement> ::= 'begin' <statement-list> 'end'
        """
        node = Node("<compound-statement>")
        
        # begin
        tok_begin = self.peek()
        if tok_begin and tok_begin.token_type == "KEYWORD" and tok_begin.value.lower() == "mulai":
            node.add_children(Node("KEYWORD", self.consume_token()))
            while True:
                tok_inner = self.peek()
                if not tok_inner or (tok_inner.token_type == "KEYWORD" and tok_inner.value.lower() == "selesai"):
                    break
                statement_node = self.parse_statement()
                if statement_node:
                    node.add_children(statement_node)
                elif self.peek() == tok_inner:
                    self.consume_token()

            end_tok = self.peek()
            if end_tok and end_tok.token_type == "KEYWORD" and end_tok.value.lower() == "selesai":
                node.add_children(Node("KEYWORD", self.consume_token()))
            else:
                self.error("KEYWORD(selesai)", end_tok)
        else:
            self.error("KEYWORD(mulai)", self.peek())


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
            self.error("expression", self.peek())
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
        tok = self.peek()
        if tok and tok.token_type == "LPARENTHESIS":
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
        
        tok = self.peek()
        if tok and tok.token_type != "RPARENTHESIS":
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
        while True:
            tok = self.peek()
            if not tok or tok.token_type != "COMMA":
                break
            comma_node = Node("COMMA", self.consume_token())
            node.add_children(comma_node)
            
            expr_node = self.parse_expression()
            if not expr_node:
                self.error("expression", self.peek())
                return None # Error, koma harus diikuti ekspresi
            node.add_children(expr_node)
            
        return node

    def parse_expression(self):
        pass
    
    def parse_simple_expression(self):
        pass

    def parse_term(self):
        """
        <term> ::= <factor> ( <multiplicative-operator> <factor> )*
        """
        node = Node("<term>")

        # first factor
        first_factor = self.parse_factor()
        if not first_factor:
            _tok = self.peek()
            self.error("factor", _tok)
            return None
        node.add_children(first_factor)

        # (* op factor)
        while True:
            op_node = self.parse_multiplicative_operator()
            if not op_node:
                break
            node.add_children(op_node)

            rhs = self.parse_factor()
            if not rhs:
                _tok2 = self.peek()
                self.error("factor", _tok2)
                return None
            node.add_children(rhs)

        return node

    def parse_factor(self):
        """
        <factor> ::= IDENTIFIER
                   | NUMBER
                   | CHAR_LITERAL
                   | STRING_LITERAL
                   | LPARENTHESIS <expression> RPARENTHESIS
                   | LOGICAL_OPERATOR(tidak) <factor>
        Catatan: Pemanggilan fungsi/prosedur (IDENTIFIER (...)) akan ditangani di rule lain
        atau dapat diperluas kemudian; di sini fokus pada bentuk-bentuk dasar sesuai permintaan.
        """
        node = Node("<factor>")
        tok = self.peek()

        if tok is None:
            self.error("factor", None)
            return None

        # unary logical NOT: 'tidak'
        if tok.token_type == "LOGICAL_OPERATOR" and tok.value.lower() == "tidak":
            not_tok = self.consume_token()
            node.add_children(Node("LOGICAL_OPERATOR", not_tok))
            sub = self.parse_factor()
            if not sub:
                _tok3 = self.peek()
                self.error("factor", _tok3)
                return None
            node.add_children(sub)
            return node

        # parenthesized expression
        if tok.token_type == "LPARENTHESIS" and tok.value == "(":
            lpar = self.consume_token()
            node.add_children(Node("LPARENTHESIS", lpar))

            expr = self.parse_expression()
            if not expr:
                _tok4 = self.peek()
                self.error("expression", _tok4)
                return None
            node.add_children(expr)

            rpar = self.match_token("RPARENTHESIS", ")")
            if not rpar:
                return None
            node.add_children(Node("RPARENTHESIS", rpar))
            return node

        # literals and identifier
        if tok.token_type in ("NUMBER", "CHAR_LITERAL", "STRING_LITERAL"):
            node.add_children(Node(tok.token_type, self.consume_token()))
            return node

        if tok.token_type == "IDENTIFIER":
            node.add_children(Node("IDENTIFIER", self.consume_token()))
            return node

        # if no form matched
        self.error("factor", tok)
        return None

    def parse_relational_operator(self):
        """
        <relational-operator> ::= '=' | '<>' | '<' | '<=' | '>' | '>='
        """
        tok = self.peek()
        if tok and tok.token_type == "RELATIONAL_OPERATOR" and tok.value in ("=", "<>", "<", "<=", ">", ">="):
            node = Node("<relational-operator>")
            node.add_children(Node("RELATIONAL_OPERATOR", self.consume_token()))
            return node
        return None

    def parse_additive_operator(self):
        """
        <additive-operator> ::= '+' | '-' | 'atau'
        '+' | '-' bertipe ARITHMETIC_OPERATOR, 'atau' bertipe LOGICAL_OPERATOR
        """
        tok = self.peek()
        if tok is None:
            return None

        if tok.token_type == "ARITHMETIC_OPERATOR" and tok.value in ("+", "-"):
            node = Node("<additive-operator>")
            node.add_children(Node("ARITHMETIC_OPERATOR", self.consume_token()))
            return node
        if tok.token_type == "LOGICAL_OPERATOR" and tok.value.lower() == "atau":
            node = Node("<additive-operator>")
            node.add_children(Node("LOGICAL_OPERATOR", self.consume_token()))
            return node
        return None

    def parse_multiplicative_operator(self):
        """
        <multiplicative-operator> ::= '*' | '/' | 'bagi' | 'mod' | 'dan'
        '*' '/' 'bagi' 'mod' bertipe ARITHMETIC_OPERATOR, 'dan' bertipe LOGICAL_OPERATOR
        """
        tok = self.peek()
        if tok is None:
            return None

        if tok.token_type == "ARITHMETIC_OPERATOR" and tok.value in ("*", "/", "bagi", "mod"):
            node = Node("<multiplicative-operator>")
            node.add_children(Node("ARITHMETIC_OPERATOR", self.consume_token()))
            return node
        if tok.token_type == "LOGICAL_OPERATOR" and tok.value.lower() == "dan":
            node = Node("<multiplicative-operator>")
            node.add_children(Node("LOGICAL_OPERATOR", self.consume_token()))
            return node
        return None