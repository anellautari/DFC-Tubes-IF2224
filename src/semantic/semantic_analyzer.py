from src.semantic.ast import *
from src.semantic.symbol_table import SymbolTables


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
    def visit_NumberLiteral(self, node: NumberLiteral):
        return node.value

    def visit_VarRef(self, node: VarRef):
        return None
