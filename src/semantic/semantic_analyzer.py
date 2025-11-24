from src.semantic.ast import *
from src.semantic.symbol_table import SymbolTables, TypeKind
from src.common.errors import SemanticError

class SemanticAnalyzer:
    def __init__(self):
        self.symtab = SymbolTables()
        self._program_visited = False

    # ================== VISITOR DISPATCH ==================
    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        fn = getattr(self, method, self.generic_visit)
        return fn(node)

    # ================== GENERIC VISIT ==================
    # Penting: Jangan traverse otomatis. Semua visit harus eksplisit.
    def generic_visit(self, node):
        return

    # ================== PROGRAM ==================
    def visit_Program(self, node: Program):
        # Pastikan program hanya diproses sekali
        if self._program_visited:
            return
        self._program_visited = True

        # Insert program name pada global scope (level 0)
        self.symtab.insert(node.name, "program", type_code=0)

        # Masuk main program block (level 1)
        node.scope_level = self.symtab.level

        # Visit block isi program
        self.visit(node.block)


    # ================== BLOCK ==================
    def visit_Block(self, node: Block):
        # Constants
        for c in node.const_decls:
            self.visit(c)

        # Types
        for t in node.type_decls:
            self.visit(t)

        # Variables
        for v in node.var_decls:
            self.visit(v)

        # Subprograms
        for s in node.subprogram_decls:
            self.visit(s)

        # Body
        if node.body:
            self.visit(node.body)

    # ================== DECLARATIONS ==================
    def visit_VarDecl(self, node: VarDecl):
        for name in node.names:
            idx = self.symtab.insert(name, "variable", 0)
            node.symbol = idx
            node.scope_level = self.symtab.level

    def visit_ConstDecl(self, node: ConstDecl):
        value = None
        if node.value:
            value = self.visit(node.value)
        idx = self.symtab.insert(node.name, "constant", type_code=0, adr=value)
        node.symbol = idx
        node.scope_level = self.symtab.level

    def visit_TypeDecl(self, node: TypeDecl):
        idx = self.symtab.insert(node.name, "type", type_code=0)
        node.symbol = idx
        node.scope_level = self.symtab.level

    # ================== PROCEDURE ==================
    def visit_ProcedureDecl(self, node: ProcedureDecl):
        # Insert procedure ke current scope
        proc_idx = self.symtab.insert(node.name, "procedure", 0)
        node.symbol = proc_idx

        # Masuk block prosedur
        self.symtab.begin_block()
        node.scope_level = self.symtab.level

        # Visit parameter (belum implement param → skip)
        for p in node.params:
            self.visit(p)

        # Visit isi block
        if node.block:
            self.visit(node.block)

        # Tutup block prosedur
        self.symtab.end_block()

    # ================== FUNCTION ==================
    def visit_FunctionDecl(self, node: FunctionDecl):
        func_idx = self.symtab.insert(node.name, "function", 0)
        node.symbol = func_idx

        self.symtab.begin_block()
        node.scope_level = self.symtab.level

        for p in node.params:
            self.visit(p)

        if node.block:
            self.visit(node.block)

        self.symtab.end_block()

    # ================== STATEMENTS ==================
    def visit_CompoundStmt(self, node: CompoundStmt):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_AssignStmt(self, node: AssignStmt):
        if node.target:
            self.visit(node.target)
        if node.value:
            self.visit(node.value)

    # =============== EXPRESSIONS ===============
    def visit_BinOp(self, node: BinOp):
        if node.left:
           left_type = self.visit(node.left)
        
        if node.right:
            right_type = self.visit(node.right)
        
        op = node.op
        
        if op in ['+', '-', '*', '/'] :
            is_real_op = (left_type == TypeKind.REALS or right_type == TypeKind.REALS or op == '/')
            
            if left_type not in (TypeKind.INTS, TypeKind.REALS) or right_type not in (TypeKind.INTS, TypeKind.REALS):
                raise SemanticError(f"Operator '{op}' memerlukan operand numerik")
            
            result = TypeKind.REALS if is_real_op else TypeKind.INTS
            node.type = result
            return result
            
        elif op in ['bagi', 'mod']:
            if left_type != TypeKind.INTS or right_type != TypeKind.INTS:
                raise SemanticError(f"Operator '{op}' hanya berlaku untuk Integer")
            node.type = TypeKind.INTS
            return TypeKind.INTS
        
        elif op in ['dan', 'atau'] :
            if left_type != TypeKind.BOOLS or right_type != TypeKind.BOOLS:
                raise SemanticError(f"Operator '{op}' memerlukan operand Boolean")
            node.type = TypeKind.BOOLS
            return TypeKind.BOOLS
        
        elif op in ['=', '<', '>', '<=', '>=', '<>', '!='] :
            if left_type != right_type:
                if {left_type, right_type} == {TypeKind.INTS, TypeKind.REALS}:
                    pass
                else:
                    raise SemanticError(f"Tipe operand tidak cocok untuk perbandingan '{op}'")
            node.type = TypeKind.BOOLS
            return TypeKind.BOOLS
        
        
    def visit_UnaryOp(self, node: UnaryOp):
        if node.operand:
            operand_type = self.visit(node.operand)
        op = node.op
        
        if op == 'tidak':
            if operand_type != TypeKind.BOOLS:
                raise SemanticError("Operator NOT butuh operand Boolean")
            return TypeKind.BOOLS
        elif op == '-':
            if operand_type not in (TypeKind.INTS, TypeKind.REALS):
                raise SemanticError("Unary Minus butuh operand numerik")
            return operand_type
        
        return operand_type

    def visit_CallExpr(self, node: CallExpr):
        entry = self.symtab.lookup(node.name)
        if entry:
            for arg in node.args:
                self.visit(arg)
        
    def visit_VarRef(self, node: VarRef):
        entry = self.symtab.lookup(node.name)
        if entry:
            if entry['kind'] == 'constant':
                return entry.get('adr')
        
        return None

    # =============== LITERALS ===============
    def visit_NumberLiteral(self, node: NumberLiteral):
        node.is_constant = True
        if '.' in node.value:
            node.type = TypeKind.REALS
            return TypeKind.REALS
        else:
            node.type = TypeKind.INTS
            return TypeKind.INTS

    def visit_StringLiteral(self, node: StringLiteral):
        node.is_constant = True
        node.type = TypeKind.STRING
        return TypeKind.STRING

    def visit_CharLiteral(self, node: CharLiteral):
        node.is_constant = True
        node.type = TypeKind.CHARS
        return TypeKind.CHARS

    def visit_BooleanLiteral(self, node: BooleanLiteral):
        node.is_constant = True
        node.type = TypeKind.REALS
        return TypeKind.BOOLS
