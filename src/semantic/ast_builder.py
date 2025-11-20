from __future__ import annotations

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
		raise NotImplementedError

	def _build_const_declaration(self, node: Node) -> list[ConstDecl]:
		raise NotImplementedError

	def _build_type_declaration(self, node: Node) -> list[TypeDecl]:
		raise NotImplementedError

	def _build_var_declaration(self, node: Node) -> list[VarDecl]:
		raise NotImplementedError

	def _build_procedure_declaration(self, node: Node) -> ProcedureDecl:
		raise NotImplementedError

	def _build_function_declaration(self, node: Node) -> FunctionDecl:
		raise NotImplementedError

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
		raise NotImplementedError

	def _build_compound_statement(self, node: Node) -> CompoundStmt:
		raise NotImplementedError

	def _build_assign_statement(self, node: Node) -> AssignStmt:
		raise NotImplementedError

	def _build_proc_call_stmt(self, node: Node) -> ProcCallStmt:
		raise NotImplementedError

	def _build_if_statement(self, node: Node) -> IfStmt:
		raise NotImplementedError

	def _build_for_statement(self, node: Node) -> ForStmt:
		raise NotImplementedError

	def _build_expression(self, node: Node) -> Expression:
		raise NotImplementedError

	def _build_simple_expression(self, node: Node) -> Expression:
		raise NotImplementedError

	def _build_term(self, node: Node) -> Expression:
		raise NotImplementedError

	def _build_factor(self, node: Node) -> Expression:
		raise NotImplementedError

	def _build_call_expr(self, node: Node) -> CallExpr:
		raise NotImplementedError

	def _collect_identifier_list(self, node: Node) -> list[str]:
		raise NotImplementedError
