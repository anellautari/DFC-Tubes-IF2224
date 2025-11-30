from src.semantic.ast import *
from src.semantic.symbol_table import SymbolTables, TypeKind, ObjectKind
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
    def generic_visit(self, node):
        return

    # ================== PROGRAM ==================
    def visit_Program(self, node: Program):
        if self._program_visited:
            return
        self._program_visited = True

        node.scope_level = self.symtab.level

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
        var_type: TypeKind = TypeKind.NOTYP

        if isinstance(node.type_expr, PrimitiveType):
            nm = node.type_expr.name.lower()
            if nm == "integer":
                var_type = TypeKind.INTS
            elif nm == "real":
                var_type = TypeKind.REALS
            elif nm == "boolean":
                var_type = TypeKind.BOOLS
            elif nm == "char":
                var_type = TypeKind.CHARS

        elif isinstance(node.type_expr, NamedType):
            ref_idx = self.symtab.lookup(node.type_expr.name)
            var_type = TypeKind.NOTYP 
        else:
            var_type = TypeKind.NOTYP

        for name in node.names:
            idx = self.symtab.insert(name, "variable", 0)
            entry = self.symtab.tab[idx]
            entry.adr = self.symtab.dx
            
            if isinstance(node.type_expr, ArrayType):
                aref = self._build_array_type(node.type_expr)
                entry.typ = TypeKind.ARRAYS
                entry.ref = aref
                self.symtab.dx += self.symtab.get_variable_size(TypeKind.ARRAYS, aref)
            else:
                entry.typ = var_type
                self.symtab.dx += self.symtab.get_variable_size(var_type)
            
            node.symbol = idx
            node.scope_level = self.symtab.level


    def visit_ConstDecl(self, node: ConstDecl):
        const_type = None
        const_value = None

        if node.value:
            const_type = self.visit(node.value)    
            if hasattr(node.value, "value"):
                const_value = node.value.value     
            node.value.type = const_type

        idx = self.symtab.insert(
            node.name,
            "constant",
            type_code=0,    
            adr=const_value
        )

        entry = self.symtab.tab[idx]
        entry.typ = const_type if const_type is not None else TypeKind.NOTYP

        node.symbol = idx
        node.scope_level = self.symtab.level


    def visit_TypeDecl(self, node: TypeDecl):
        idx = self.symtab.insert(node.name, "type", type_code=0)
        entry = self.symtab.tab[idx]

        if isinstance(node.type_expr, PrimitiveType):
            name = node.type_expr.name.lower()
            if name == "integer":
                entry.typ = TypeKind.INTS
            elif name == "real":
                entry.typ = TypeKind.REALS
            elif name == "boolean":
                entry.typ = TypeKind.BOOLS
            elif name == "char":
                entry.typ = TypeKind.CHARS

        elif isinstance(node.type_expr, NamedType):
            entry.typ = TypeKind.NOTYP
            entry.ref = self.symtab.lookup(node.type_expr.name)

        elif isinstance(node.type_expr, ArrayType):
            aref = self._build_array_type(node.type_expr)
            entry.typ = TypeKind.ARRAYS
            entry.ref = aref

        node.symbol = idx

    # ================== PROCEDURE ==================
    def visit_ProcedureDecl(self, node: ProcedureDecl):
        # Insert procedure ke current scope
        proc_idx = self.symtab.insert(node.name, "procedure", 0)
        node.symbol = proc_idx
        proc_entry = self.symtab.tab[proc_idx]

        # Masuk block prosedur
        block_idx = self.symtab.begin_block()
        proc_entry.ref = block_idx  # Store block reference for parameter lookup
        node.scope_level = self.symtab.level

        # Visit parameter
        for p in node.params:
            self.visit(p)
        self.symtab.mark_parameter_section_end()

        # Visit isi block
        if node.block:
            self.visit(node.block)

        # Tutup block prosedur
        self.symtab.end_block()

    # ================== FUNCTION ==================
    def visit_Param(self, node: Param):
        idx = self.symtab.insert(node.name, "variable", 0)
        entry = self.symtab.tab[idx]
        
        entry.adr = self.symtab.dx
        
        entry.typ = TypeKind.NOTYP   
        entry.nrm = True
        node.symbol = idx
        node.scope_level = self.symtab.level

        if isinstance(node.type_expr, PrimitiveType):
            nm = node.type_expr.name.lower()
            if nm == "integer":
                entry.typ = TypeKind.INTS
            elif nm == "real":
                entry.typ = TypeKind.REALS
            elif nm == "boolean":
                entry.typ = TypeKind.BOOLS
            elif nm == "char":
                entry.typ = TypeKind.CHARS
        
        self.symtab.dx += self.symtab.get_variable_size(entry.typ)


    def visit_FunctionDecl(self, node: FunctionDecl):
        func_idx = self.symtab.insert(node.name, "function", 0)
        func_entry = self.symtab.tab[func_idx]
        node.symbol = func_idx

        ret_type: TypeKind = TypeKind.NOTYP
        if isinstance(node.return_type, PrimitiveType):
            nm = node.return_type.name.lower()
            if nm == "integer":
                ret_type = TypeKind.INTS
            elif nm == "real":
                ret_type = TypeKind.REALS
            elif nm == "char":
                ret_type = TypeKind.CHARS
            elif nm == "boolean":
                ret_type = TypeKind.BOOLS

        func_entry.typ = ret_type

        self.symtab.begin_block()
        node.scope_level = self.symtab.level

        implicit_idx = self.symtab.insert(node.name, "variable", 0)
        implicit_entry = self.symtab.tab[implicit_idx]
        implicit_entry.typ = ret_type
        implicit_entry.adr = self.symtab.dx
        self.symtab.dx += self.symtab.get_variable_size(ret_type)

        for p in node.params:
            self.visit(p)

        self.symtab.mark_parameter_section_end()

        if node.block:
            self.visit(node.block)

        self.symtab.end_block()

    # ================== ARRAY TYPE BUILDING ==================
    def _type_from_primitive(self, prim: PrimitiveType):
        nm = prim.name.lower()
        if nm == "integer":
            return TypeKind.INTS
        if nm == "real":
            return TypeKind.REALS
        if nm == "boolean":
            return TypeKind.BOOLS
        if nm == "char":
            return TypeKind.CHARS
        return TypeKind.NOTYP

    def _const_value(self, expr):
        t = self.visit(expr)
        if hasattr(expr, "evaluated_value") and expr.evaluated_value is not None:
            try:
                return int(expr.evaluated_value)
            except Exception:
                return None
        if hasattr(expr, "value"):
            v = expr.value
            if t == TypeKind.CHARS and isinstance(v, str) and len(v) == 1:
                return ord(v)
            if isinstance(v, bool):
                return int(bool(v))
            try:
                return int(v)
            except Exception:
                return None
        return None

    def _index_type_from_bounds(self, lt: TypeKind, ut: TypeKind) -> TypeKind:
        if lt == ut == TypeKind.INTS:
            return TypeKind.INTS
        if lt == ut == TypeKind.CHARS:
            return TypeKind.CHARS
        return TypeKind.NOTYP

    def _build_array_type(self, arr: ArrayType) -> int:
        idx_range = arr.index_range
        if idx_range is None:
            raise SemanticError("Array type requires index range")
        ltype = self.visit(idx_range.lower) if idx_range.lower else None
        utype = self.visit(idx_range.upper) if idx_range.upper else None
        inx_type = self._index_type_from_bounds(ltype, utype)
        low = self._const_value(idx_range.lower)
        high = self._const_value(idx_range.upper)
        aref = self.symtab.enter_array(inx_type, low, high)

        elem_t = TypeKind.NOTYP
        elem_ref = 0
        elem_size = 1
        if isinstance(arr.element_type, PrimitiveType):
            elem_t = self._type_from_primitive(arr.element_type)
            elem_size = self.symtab.get_elem_size(elem_t)
        elif isinstance(arr.element_type, ArrayType):
            elem_ref = self._build_array_type(arr.element_type)
            elem_t = TypeKind.ARRAYS
            elem_size = self.symtab.get_elem_size(elem_t, elem_ref)
        elif isinstance(arr.element_type, NamedType):
            ref_idx = self.symtab.lookup(arr.element_type.name)
            if ref_idx is not None:
                ref_entry = self.symtab.tab[ref_idx]
                elem_t = ref_entry.typ
                elem_ref = ref_entry.ref
                elem_size = self.symtab.get_elem_size(elem_t, elem_ref)

        self.symtab.finalize_array(aref, elem_t, elem_ref, elem_size)
        return aref

    # ================== STATEMENTS ==================
    def visit_CompoundStmt(self, node: CompoundStmt):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_AssignStmt(self, node: AssignStmt):
        var_name = node.target.name
        var_idx = self.symtab.lookup(var_name)
        
        if var_idx is None:
            raise SemanticError(f"Variable '{var_name}' not declared.")
            
        var_entry = self.symtab.tab[var_idx]
        
        if var_entry.obj not in (ObjectKind.VARIABLE, ObjectKind.FUNCTION):
            raise SemanticError(
                f"Cannot assign to '{var_name}' because it is a {var_entry.obj}.",
            )

        expr_type = self.visit(node.value)
        
        if expr_type and var_entry.typ != expr_type:
           raise SemanticError(f"Type mismatch in assignment. Cannot assign {expr_type} to variable '{var_name}' of type {var_entry.typ}.")

    def visit_IfStmt(self, node: IfStmt):
        condition_type = self.visit(node.condition)
        if condition_type is not None and condition_type != TypeKind.BOOLS:
            raise SemanticError("If condition must be of boolean expression.")
            
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visit_WhileStmt(self, node: WhileStmt):
        condition_type = self.visit(node.condition)
        if condition_type is not None and condition_type != TypeKind.BOOLS:
            raise SemanticError("While condition must be of boolean expression.")
        
        self.visit(node.body)

    def visit_ForStmt(self, node: ForStmt):
        var_name = node.var.name
        var_idx = self.symtab.lookup(var_name)
        
        if var_idx is None:
            raise SemanticError(f"Loop variable '{var_name}' not declared.")
            
        var_entry = self.symtab.tab[var_idx]
        if var_entry.typ != TypeKind.INTS:
            raise SemanticError(f"For loop variable '{var_name}' must be of type integer.")
        
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
		
		# Start dan End harus Integer
        if start_type is not None and start_type != TypeKind.INTS:
            raise SemanticError("For loop start expression must be Integer.")
			
        if end_type is not None and end_type != TypeKind.INTS:
            raise SemanticError("For loop end expression must be Integer.")
			
        self.visit(node.body)

    def visit_ProcCallStmt(self, node: ProcCallStmt):
        proc_name = node.name
        proc_idx = self.symtab.lookup(proc_name)
        
        if proc_idx is None:
            raise SemanticError(f"Procedure '{proc_name}' not declared.")
            
        proc_entry = self.symtab.tab[proc_idx]
        
        if proc_entry.obj != ObjectKind.PROCEDURE:
            raise SemanticError(f"'{proc_name}' is not a procedure.")
        
        arg_types = []
        for arg in node.args:
            arg_type = self.visit(arg)
            arg_types.append(arg_type)
        
        if proc_entry.ref == 0 and proc_entry.adr in (1, 2, 3, 4):
            return
        
        param_types = self._get_procedure_param_types(proc_entry.ref)
        
        # Check argument count
        if len(arg_types) != len(param_types):
            raise SemanticError(
                f"Procedure '{proc_name}' expects {len(param_types)} argument(s), but got {len(arg_types)}."
            )
        
        # Check argument types match parameter types
        for i, (arg_type, param_type) in enumerate(zip(arg_types, param_types)):
            if arg_type != param_type:
                if not (param_type == TypeKind.REALS and arg_type == TypeKind.INTS):
                    raise SemanticError(
                        f"Type mismatch in argument {i+1} of procedure '{proc_name}'. "
                        f"Expected {param_type}, but got {arg_type}."
                    )
    
    def _get_procedure_param_types(self, block_ref: int) -> list:
        if block_ref <= 0 or block_ref >= len(self.symtab.btab):
            return []
        
        block = self.symtab.btab[block_ref]
        last_param = block.lpar
        
        if last_param == 0:
            return []
        
        params = []
        ptr = last_param
        while ptr != 0:
            entry = self.symtab.tab[ptr]
            if entry.lev == self.symtab.level + 1 or entry.lev == block_ref:
                params.append(entry.typ)
            ptr = entry.link
        
        # Reverse to get correct order
        params.reverse()
        return params

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
        idx = self.symtab.lookup(node.name)
        if idx is None:
            raise SemanticError(f"Undefined identifier '{node.name}'")

        entry = self.symtab.tab[idx]

        node.symbol = idx
        node.scope_level = entry.lev
        node.type = entry.typ

        return entry.typ

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
        node.type = TypeKind.STRINGS
        return TypeKind.STRINGS

    def visit_CharLiteral(self, node: CharLiteral):
        node.is_constant = True
        node.type = TypeKind.CHARS
        return TypeKind.CHARS

    def visit_BooleanLiteral(self, node: BooleanLiteral):
        node.is_constant = True
        node.type = TypeKind.BOOLS
        return TypeKind.BOOLS
