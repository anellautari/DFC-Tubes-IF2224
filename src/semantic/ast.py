from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from src.common.pascal_token import Token


@dataclass
class ASTNode:
	"""Base AST node carrying source token and semantic placeholders."""

	token: Token | None = None
	type_info: Any | None = None
	symbol: Any | None = None
	scope_level: int | None = None


class Statement(ASTNode):
	"""Marker base class for statement nodes."""


class Expression(ASTNode):
	"""Marker base class for expression nodes."""


class TypeExpr(ASTNode):
	"""Marker base class for type expression nodes."""


class SubprogramDecl(ASTNode):
	"""Base class for procedure/function declarations."""


class ParamKind(Enum):
	VALUE = "value"


class ForDirection(Enum):
	TO = "ke"
	DOWNTO = "turun_ke"


@dataclass
class Program(ASTNode):
	name: str = ""
	block: Block | None = None


@dataclass
class Block(ASTNode):
	const_decls: list["ConstDecl"] = field(default_factory=list)
	type_decls: list["TypeDecl"] = field(default_factory=list)
	var_decls: list["VarDecl"] = field(default_factory=list)
	subprogram_decls: list[SubprogramDecl] = field(default_factory=list)
	body: CompoundStmt | None = None


@dataclass
class ConstDecl(ASTNode):
	name: str = ""
	value: Expression | None = None


@dataclass
class TypeDecl(ASTNode):
	name: str = ""
	type_expr: TypeExpr | None = None


@dataclass
class VarDecl(ASTNode):
	names: list[str] = field(default_factory=list)
	type_expr: TypeExpr | None = None


@dataclass
class Param(ASTNode):
	name: str = ""
	type_expr: TypeExpr | None = None
	kind: ParamKind = ParamKind.VALUE


@dataclass
class ProcedureDecl(SubprogramDecl):
	name: str = ""
	params: list[Param] = field(default_factory=list)
	block: Block | None = None


@dataclass
class FunctionDecl(SubprogramDecl):
	name: str = ""
	params: list[Param] = field(default_factory=list)
	return_type: TypeExpr | None = None
	block: Block | None = None


@dataclass
class PrimitiveType(TypeExpr):
	name: str = ""


@dataclass
class NamedType(TypeExpr):
	name: str = ""


@dataclass
class RangeExpr(ASTNode):
	lower: Expression | None = None
	upper: Expression | None = None


@dataclass
class ArrayType(TypeExpr):
	index_range: RangeExpr | None = None
	element_type: TypeExpr | None = None


@dataclass
class CompoundStmt(Statement):
	statements: list[Statement] = field(default_factory=list)


@dataclass
class AssignStmt(Statement):
	target: VarRef | None = None
	value: Expression | None = None


@dataclass
class IfStmt(Statement):
	condition: Expression | None = None
	then_branch: Statement | None = None
	else_branch: Statement | None = None


@dataclass
class WhileStmt(Statement):
	condition: Expression | None = None
	body: Statement | None = None


@dataclass
class ForStmt(Statement):
	var: VarRef | None = None
	start: Expression | None = None
	end: Expression | None = None
	direction: ForDirection = ForDirection.TO
	body: Statement | None = None


@dataclass
class ProcCallStmt(Statement):
	name: str = ""
	args: list[Expression] = field(default_factory=list)


@dataclass
class CallExpr(Expression):
	name: str = ""
	args: list[Expression] = field(default_factory=list)


@dataclass
class BinOp(Expression):
	op: str = ""
	left: Expression | None = None
	right: Expression | None = None


@dataclass
class UnaryOp(Expression):
	op: str = ""
	operand: Expression | None = None


@dataclass
class VarRef(Expression):
	name: str = ""


@dataclass
class NumberLiteral(Expression):
	value: str = ""


@dataclass
class StringLiteral(Expression):
	value: str = ""


@dataclass
class CharLiteral(Expression):
	value: str = ""


@dataclass
class BooleanLiteral(Expression):
	value: bool | str | None = None

