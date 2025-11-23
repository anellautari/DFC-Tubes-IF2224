from src.semantic.ast import *
from src.semantic.symbol_table import SymbolTables
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
        var_name = node.target.name
        var_idx = self.symtab.lookup(var_name)
        
        if var_idx is None:
            raise SemanticError(f"Variable '{var_name}' not declared.", node.token)
            
        var_entry = self.symtab.tab[var_idx]
        
        if var_entry.obj != "variable" and var_entry.obj != "function":
             raise SemanticError(f"Cannot assign to '{var_name}' because it is a {var_entry.obj}.", node.token)

        expr_type = self.visit(node.value)
        
        if expr_type and var_entry.typ != expr_type:
           raise SemanticError(f"Type mismatch in assignment. Cannot assign {expr_type} to variable '{var_name}' of type {var_entry.typ}.", node.token)

    def visit_IfStmt(self, node: IfStmt):
        condition_type = self.visit(node.condition)
        if condition_type is not None and condition_type != "bools":
            raise SemanticError("If condition must be of boolean expression.", node.token)
            
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visit_WhileStmt(self, node: WhileStmt):
        condition_type = self.visit(node.condition)
        if condition_type is not None and condition_type != "bools":
            raise SemanticError("While condition must be of boolean expression.", node.token)
        
        self.visit(node.body)

    def visit_ForStmt(self, node: ForStmt):
        var_name = node.var.name
        var_idx = self.symtab.lookup(var_name)
        
        if var_idx is None:
            raise SemanticError(f"Loop variable '{var_name}' not declared.", node.token)
            
        var_entry = self.symtab.tab[var_idx]
        if var_entry.typ != "ints":
            raise SemanticError(f"For loop variable '{var_name}' must be of type integer.", node.token)
        
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
		
		# Start dan End harus Integer
        if start_type is not None and start_type != "ints":
            raise SemanticError("For loop start expression must be Integer.", node.token)
			
        if end_type is not None and end_type != "ints":
            raise SemanticError("For loop end expression must be Integer.", node.token)
			
        self.visit(node.body)

    def visit_ProcCallStmt(self, node: ProcCallStmt):
        proc_name = node.name
        proc_idx = self.symtab.lookup(proc_name)
        
        if proc_idx is None:
            raise SemanticError(f"Procedure '{proc_name}' not declared.", node.token)
            
        proc_entry = self.symtab.tab[proc_idx]
        
        if proc_entry.obj != "procedure":
            raise SemanticError(f"'{proc_name}' is not a procedure.", node.token)
            
        # Validasi Argumen
        for arg in node.args:
            self.visit(arg)

    # =============== EXPRESSIONS ===============
    def visit_NumberLiteral(self, node: NumberLiteral):
        return node.value

    def visit_VarRef(self, node: VarRef):
        return None
