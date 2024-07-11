from abc import ABC, abstractmethod
from typing import Any
from token import Token
from visitor import Visitor
from expr import Expr

class Stmt(ABC):

	def __repr__(self):
		return (type(self).__name__) + str(self.__dict__)

	@abstractmethod
	def accept(self, visitor: Visitor):
		pass

class Block(Stmt):
	def __init__(self, statements: list[Stmt]):
		self.statements = statements

	def accept(self, visitor: Visitor):
		return visitor.visit_block_stmt(self)

class Expression(Stmt):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: Visitor):
		return visitor.visit_expression_stmt(self)

class Print(Stmt):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: Visitor):
		return visitor.visit_print_stmt(self)

class Var(Stmt):
	def __init__(self, name: Token, initializer: Expr):
		self.name = name
		self.initializer = initializer

	def accept(self, visitor: Visitor):
		return visitor.visit_var_stmt(self)

