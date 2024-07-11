from abc import ABC, abstractmethod
from typing import Any
from token import Token
from visitor import Visitor

class Expr(ABC):

	def __repr__(self):
		return (type(self).__name__) + str(self.__dict__)

	@abstractmethod
	def accept(self, visitor: Visitor):
		pass

class Assign(Expr):
	def __init__(self, name: Token, value: Expr):
		self.name = name
		self.value = value

	def accept(self, visitor: Visitor):
		return visitor.visit_assign_expr(self)

class Binary(Expr):
	def __init__(self, left: Expr, operator: Token, right: Expr):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor: Visitor):
		return visitor.visit_binary_expr(self)

class Grouping(Expr):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: Visitor):
		return visitor.visit_grouping_expr(self)

class Literal(Expr):
	def __init__(self, value: Any):
		self.value = value

	def accept(self, visitor: Visitor):
		return visitor.visit_literal_expr(self)

class Unary(Expr):
	def __init__(self, operator: Token, right: Expr):
		self.operator = operator
		self.right = right

	def accept(self, visitor: Visitor):
		return visitor.visit_unary_expr(self)

class Variable(Expr):
	def __init__(self, name: Token):
		self.name = name

	def accept(self, visitor: Visitor):
		return visitor.visit_variable_expr(self)

