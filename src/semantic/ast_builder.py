from __future__ import annotations
from typing import List

from src.common import node
from src.common.node import Node
from src.semantic.ast import (
	ArrayType,
	AssignStmt,
	Block,
	CallExpr,
	CompoundStmt,
	ConstDecl,
	Expression,
	ForStmt,
	FunctionDecl,
	IfStmt,
	Param,
	ProcedureDecl,
	ProcCallStmt,
	Program,
	RangeExpr,
	Statement,
	TypeDecl,
	TypeExpr,
	VarDecl,
	WhileStmt,
	VarRef,
	ForDirection,
	BinOp,
	UnaryOp,
	NumberLiteral,
	StringLiteral,
	CharLiteral,
	BooleanLiteral,
)


class ASTBuilder:
	"""Provides helpers to transform parser Nodes into semantic AST nodes."""

	def build(self, root: Node) -> Program:
		"""Build a Program AST node from the parser root."""
		raise NotImplementedError

	def _build_program(self, node: Node) -> Program:
		raise NotImplementedError

	def _build_block(self, node: Node) -> Block:
		raise NotImplementedError

	def _build_declaration_part(self, node: Node, block: Block) -> None:
		"""Populate a Block with declarations found under <declaration-part>."""
		for child in node.children:
			match child.label:
				case "<const-declaration>":
					block.const_decls.extend(self._build_const_declaration(child))
				case "<type-declaration>":
					block.type_decls.extend(self._build_type_declaration(child))
				case "<var-declaration>":
					block.var_decls.extend(self._build_var_declaration(child))
				case "<procedure-declaration>":
					block.subprogram_decls.append(self._build_procedure_declaration(child))
				case "<function-declaration>":
					block.subprogram_decls.append(self._build_function_declaration(child))

	def _build_const_declaration(self, node: Node) -> list[ConstDecl]:
		"""Build list[ConstDecl] from <const-declaration> node.

		Structure (after leading KEYWORD "konstanta"):
		  IDENTIFIER '=' <expression> ';' (repeated)
		"""
		decls: list[ConstDecl] = []
		children = node.children
		# Skip the first child (KEYWORD 'konstanta') if present
		start_index = 1 if children and children[0].label == "KEYWORD" else 0
		i = start_index
		while i < len(children):
			# Expect IDENTIFIER
			ident_node = children[i] if i < len(children) else None
			if not ident_node or ident_node.label != "IDENTIFIER" or ident_node.token is None:
				break
				
			name = ident_node.token.value
			i += 1  # move past IDENTIFIER
			# '='
			if i < len(children) and children[i].label == "RELATIONAL_OPERATOR":
				i += 1
			# Expression node
			expr_node = children[i] if i < len(children) else None
			value_expr = None
			if expr_node and expr_node.label == "<expression>":
				try:
					value_expr = self._build_expression(expr_node)
				except NotImplementedError:
					value_expr = None
				i += 1
			# Trailing semicolon
			if i < len(children) and children[i].label == "SEMICOLON":
				i += 1
			decls.append(ConstDecl(name=name, value=value_expr, token=ident_node.token))
		return decls

	def _build_type_declaration(self, node: Node) -> list[TypeDecl]:
		"""Build list[TypeDecl] from <type-declaration> node.

		Pattern (after KEYWORD 'tipe'):
		  IDENTIFIER '=' <type> ';' (repeated)
		"""
		decls: list[TypeDecl] = []
		children = node.children
		start_index = 1 if children and children[0].label == "KEYWORD" else 0
		i = start_index
		while i < len(children):
			ident_node = children[i] if i < len(children) else None
			if not ident_node or ident_node.label != "IDENTIFIER" or ident_node.token is None:
				break
			name = ident_node.token.value
			i += 1
			# '='
			if i < len(children) and children[i].label == "RELATIONAL_OPERATOR":
				i += 1
			# <type>
			type_node = children[i] if i < len(children) else None
			built_type = None
			if type_node and type_node.label == "<type>":
				try:
					built_type = self._build_type_expr(type_node)
				except NotImplementedError:
					built_type = None
				i += 1
			# ';'
			if i < len(children) and children[i].label == "SEMICOLON":
				i += 1
			decls.append(TypeDecl(name=name, type_expr=built_type, token=ident_node.token))
		return decls

	def _build_var_declaration(self, node: Node) -> list[VarDecl]:
		"""Build list[VarDecl] from <var-declaration> node.

		Pattern (after KEYWORD 'variabel'):
		  <identifier-list> ':' <type> ';' (repeated)
		Each group becomes one VarDecl (names share the same type).
		"""
		decls: list[VarDecl] = []
		children = node.children
		start_index = 1 if children and children[0].label == "KEYWORD" else 0
		i = start_index
		while i < len(children):
			id_list_node = children[i] if i < len(children) else None
			if not id_list_node or id_list_node.label != "<identifier-list>":
				break
			# Collect identifiers
			try:
				names = self._collect_identifier_list(id_list_node)
			except NotImplementedError:
				names = []
			i += 1
			# ':'
			if i < len(children) and children[i].label == "COLON":
				i += 1
			# <type>
			type_node = children[i] if i < len(children) else None
			built_type = None
			if type_node and type_node.label == "<type>":
				try:
					built_type = self._build_type_expr(type_node)
				except NotImplementedError:
					built_type = None
				i += 1
			# ';'
			if i < len(children) and children[i].label == "SEMICOLON":
				i += 1
			decls.append(VarDecl(names=names, type_expr=built_type, token=id_list_node.token))
		return decls

	def _build_procedure_declaration(self, node: Node) -> ProcedureDecl:
		"""Build a ProcedureDecl from <procedure-declaration>.

		Structure:
		  KEYWORD('prosedur') IDENTIFIER [ <formal-parameter-list> ] ';' <block> ';'
		"""
		name: str = ""
		params: list[Param] = []
		blk: Block | None = None
		ident_token = None
		for child in node.children:
			if child.label == "IDENTIFIER" and ident_token is None and child.token:
				ident_token = child.token
				name = ident_token.value
			elif child.label == "<formal-parameter-list>":
				try:
					params = self._build_formal_parameter_list(child)  # type: ignore[arg-type]
				except NotImplementedError:
					params = []
			elif child.label == "<block>":
				try:
					blk = self._build_block(child)  # type: ignore[arg-type]
				except NotImplementedError:
					blk = None
		return ProcedureDecl(name=name, params=params, block=blk, token=ident_token)

	def _build_function_declaration(self, node: Node) -> FunctionDecl:
		"""Build a FunctionDecl from <function-declaration> node.

		Structure:
		  KEYWORD('fungsi') IDENTIFIER [ <formal-parameter-list> ] ':' <type> ';' <block> ';'
		"""
		name: str = ""
		params: list[Param] = []
		ret_type: TypeExpr | None = None
		blk: Block | None = None
		ident_token = None
		after_colon = False
		for child in node.children:
			if child.label == "IDENTIFIER" and ident_token is None and child.token:
				ident_token = child.token
				name = ident_token.value
			elif child.label == "<formal-parameter-list>":
				try:
					params = self._build_formal_parameter_list(child)  # type: ignore[arg-type]
				except NotImplementedError:
					params = []
			elif child.label == "COLON":
				after_colon = True
			elif child.label == "<type>" and after_colon:
				try:
					ret_type = self._build_type_expr(child)
				except NotImplementedError:
					ret_type = None
			elif child.label == "<block>":
				try:
					blk = self._build_block(child)
				except NotImplementedError:
					blk = None
		return FunctionDecl(name=name, params=params, return_type=ret_type, block=blk, token=ident_token)

	def _build_formal_parameter_list(self, node: Node) -> list[Param]:
		raise NotImplementedError

	def _build_parameter_group(self, node: Node) -> list[Param]:
		raise NotImplementedError

	def _build_type_expr(self, node: Node) -> TypeExpr:
		raise NotImplementedError

	def _build_array_type(self, node: Node) -> ArrayType:
		raise NotImplementedError

	def _build_range_expr(self, node: Node) -> RangeExpr:
		raise NotImplementedError

	def _build_statement(self, node: Node) -> Statement:
		"""Dispatch to specific statement builders based on the node label.
  
		Handles:
		- Compound statements
		- Assignment statements
		- Procedure/function call statements
		- If statements
		- While statements
		- For statements
  		"""
		if node.label == "<assignment-statement>":
			return self._build_assign_statement(node)
			
		elif node.label == "<procedure-function-call>": # Sesuaikan label dari parser M2
			return self._build_proc_call_stmt(node)
			
		elif node.label == "<if-statement>":
			return self._build_if_statement(node)
			
		elif node.label == "<while-statement>":
			return self._build_while_statement(node)
			
		elif node.label == "<for-statement>":
			return self._build_for_statement(node)
			
		elif node.label == "<compound-statement>":
			return self._build_compound_statement(node)

		if node.children:
			first_child = node.children[0] 
			if first_child.label == "KEYWORD" and first_child.token:
				kw = first_child.token.value.lower()
				match kw:
					case "mulai":
						return self._build_compound_statement(node)
					case "jika":
						return self._build_if_statement(node)
					case "selama":
						return self._build_while_statement(node)
					case "untuk":
						return self._build_for_statement(node)

			elif first_child.label == "<assignment-statement>":
				return self._build_assign_statement(first_child)

			elif first_child.label == "<procedure-function-call>":
				return self._build_proc_call_stmt(first_child)

		raise NotImplementedError(f"Unknown statement type: {first_child.label}")


	def _build_compound_statement(self, node: Node) -> CompoundStmt:
		"""Build a CompoundStmt from <compound-statement> node.
		
  		Structure:
		  KEYWORD('mulai') <statement-list> KEYWORD('selesai')
		"""
		stmts: list[Statement] = []
		for child in node.children:
			if child.label in ["KEYWORD", "SEMICOLON"]:
				continue	
			stmts.append(self._build_statement(child))
			
		return CompoundStmt(statements=stmts, token=node.children[0].token)

	def _build_assign_statement(self, node: Node) -> AssignStmt:
		"""Build an AssignStmt from <assignment-statement> node.
  
		Structure:
		  IDENTIFIER ASSIGN_OPERATOR(:=) <expression>
  		"""
		target_token = node.children[0].token
		target_ref = VarRef(name=target_token.value, token=target_token)
		assign_token = node.children[1].token
		expr_node = node.children[2]
		value_expr = self._build_expression(expr_node)
		
		return AssignStmt(target=target_ref, value=value_expr, token=assign_token)

	def _build_proc_call_stmt(self, node: Node) -> ProcCallStmt:
		"""Build a ProcCallStmt from <procedure-function-call> node.

		Structure:
		  IDENTIFIER [ LPAREN <parameter-list> RPAREN ]
		"""
		ident_token = node.children[0].token
		name = ident_token.value
		args = []
		if len(node.children) > 1 and node.children[1].label == "LPARENTHESIS":
			param_list_node = node.children[2]
			for child in param_list_node.children:
				if child.label == "<expression>":
					args.append(self._build_expression(child))
					
		return ProcCallStmt(name=name, args=args, token=ident_token)

	def _build_if_statement(self, node: Node) -> IfStmt:
		"""Build an IfStmt from <if-statement> node.
  
		Structure:
		  KEYWORD(jika) <expression> KEYWORD(maka) <statement> [KEYWORD(selain_itu) <statement>]
  		"""
		if_token = node.children[0].token
		condition = self._build_expression(node.children[1])
		then_branch = self._build_statement(node.children[3])
		else_branch = None
		if len(node.children) > 4:
			else_branch = self._build_statement(node.children[5])
			
		return IfStmt(condition=condition, then_branch=then_branch, else_branch=else_branch, token=if_token)

	def _build_for_statement(self, node: Node) -> ForStmt:
		"""Build a ForStmt from <for-statement> node.

		Structure:
		  KEYWORD(untuk) IDENTIFIER ASSIGN_OPERATOR <expression> (ke/turun_ke) <expression> KEYWORD(lakukan) <statement>
  		"""
		for_token = node.children[0].token
		var_token = node.children[1].token
		var_ref = VarRef(name=var_token.value, token=var_token)
		start_expr = self._build_expression(node.children[3])
		dir_node = node.children[4]
		direction = ForDirection.TO
		if dir_node.token.value == "turun_ke":
			direction = ForDirection.DOWNTO
			
		end_expr = self._build_expression(node.children[5])
		body = self._build_statement(node.children[7])
		
		return ForStmt(var=var_ref, start=start_expr, end=end_expr, direction=direction, body=body, token=for_token)

	def _build_while_statement(self, node: Node) -> WhileStmt:
		"""Build a WhileStmt from <while-statement> node.
  
		Structure: 
		  KEYWORD(selama) <expression> KEYWORD(lakukan) <statement>
		"""
		while_token = node.children[0].token
		condition = self._build_expression(node.children[1])
		body = self._build_statement(node.children[3])
		
		return WhileStmt(condition=condition, body=body, token=while_token)
  

	def _build_expression(self, node: Node) -> Expression:
		"""
		expression -> <simple-expression> [ <relational-operator> <simple-expression> ]
		"""
		children = node.children
		
		if not children or children[0].label != "<simple-expression>":
			raise NotImplementedError("expression without simple-expression")
		
		left = self._build_simple_expression(children[0])
		
		if len(children) >= 3 and children[1].label == "<relational-operator>":
			op_node = children[1]
			if op_node.children and op_node.children[0].token:
				op = op_node.children[0].token.value
			else:
				op = "="
			
			right = self._build_simple_expression(children[2])
			return BinOp(op=op, left=left, right=right, token=node.token)
		
		return left

	def _build_simple_expression(self, node: Node) -> Expression:
		"""
		simple-expression -> [ SIGN ] <term> { <additive-operator> <term> }
		"""
		children = node.children
		i = 0
		
		unary_sign = None
		if children and children[0].label == "SIGN":
			if children[0].token:
				unary_sign = children[0].token.value
			i += 1
		
		if i >= len(children) or children[i].label != "<term>":
			raise NotImplementedError("simple-expression without term")
		
		left = self._build_term(children[i])
		
		if unary_sign:
			left = UnaryOp(op=unary_sign, operand=left, token=children[0].token)
		
		i += 1
		
		while i < len(children):
			if children[i].label != "<additive-operator>":
				break
			
			op_node = children[i]
			if op_node.children and op_node.children[0].token:
				op = op_node.children[0].token.value
			else:
				op = "+"
			
			i += 1
			
			if i >= len(children) or children[i].label != "<term>":
				break
			
			right = self._build_term(children[i])
			left = BinOp(op=op, left=left, right=right, token=op_node.token)
			i += 1
		
		return left

	def _build_term(self, node: Node) -> Expression:
		"""
		term -> <factor> { <multiplicative-operator> <factor> }
		"""
		children = node.children
		
		if not children or children[0].label != "<factor>":
			raise NotImplementedError("term without factor")
		
		left = self._build_factor(children[0])
		i = 1
		
		while i < len(children):
			if children[i].label != "<multiplicative-operator>":
				break
			
			op_node = children[i]
			if op_node.children and op_node.children[0].token:
				op = op_node.children[0].token.value
			else:
				op = "*"
			
			i += 1
			
			if i >= len(children) or children[i].label != "<factor>":
				break
			
			right = self._build_factor(children[i])
			left = BinOp(op=op, left=left, right=right, token=op_node.token)
			i += 1
		
		return left

	def _build_factor(self, node: Node) -> Expression:
		"""
		factor -> IDENTIFIER
		        | <procedure-function-call>
		        | NUMBER
		        | CHAR_LITERAL
		        | STRING_LITERAL
		        | LPARENTHESIS <expression> RPARENTHESIS
		        | LOGICAL_OPERATOR('tidak') <factor>
		"""
		children = node.children
		
		if not children:
			raise NotImplementedError("empty factor")
		
		first_child = children[0]
		
		if first_child.label == "NUMBER" and first_child.token:
			return NumberLiteral(value=first_child.token.value, token=first_child.token)
		
		if first_child.label == "STRING_LITERAL" and first_child.token:
			return StringLiteral(value=first_child.token.value, token=first_child.token)
		
		if first_child.label == "CHAR_LITERAL" and first_child.token:
			return CharLiteral(value=first_child.token.value, token=first_child.token)
		
		if first_child.label == "BOOLEAN_LITERAL" and first_child.token:
			val = first_child.token.value.lower() == "true"
			return BooleanLiteral(value=val, token=first_child.token)
		
		if first_child.label == "LOGICAL_OPERATOR" and first_child.token:
			if first_child.token.value.lower() == "tidak":
				if len(children) < 2 or children[1].label != "<factor>":
					raise NotImplementedError("'tidak' without factor")
				operand = self._build_factor(children[1])
				return UnaryOp(op="tidak", operand=operand, token=first_child.token)
		
		if first_child.label == "LPARENTHESIS":
			expr_node = next((c for c in children if c.label == "<expression>"), None)
			if not expr_node:
				raise NotImplementedError("parenthesized factor without expression")
			return self._build_expression(expr_node)
		
		if first_child.label == "<procedure-function-call>":
			return self._build_call_expr(first_child)
		
		if first_child.label == "IDENTIFIER" and first_child.token:
			return VarRef(name=first_child.token.value, token=first_child.token)
		
		raise NotImplementedError(f"unhandled factor type: {first_child.label}")

	def _build_call_expr(self, node: Node) -> CallExpr:
		"""
		Build CallExpr from <procedure-function-call>
		"""
		name = ""
		args: list[Expression] = []
		ident_token = None
		
		for child in node.children:
			if child.label == "IDENTIFIER" and child.token:
				name = child.token.value
				ident_token = child.token
			elif child.label == "<parameter-list>":
				for param_child in child.children:
					if param_child.label == "<expression>":
						try:
							arg_expr = self._build_expression(param_child)
							args.append(arg_expr)
						except NotImplementedError:
							pass
		
		return CallExpr(name=name, args=args, token=ident_token)

	def _collect_identifier_list(self, node: Node) -> List[str]:
		"""
		Collect identifier strings from <identifier-list>
		"""
		identifiers = []
		for child in node.children:
			if child.label == "IDENTIFIER" and child.token:
				identifiers.append(child.token.value)
		return identifiers