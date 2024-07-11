from abc import ABC, abstractmethod

class Visitor(ABC):

	@abstractmethod
	def visit_assign_expr(self, expr):
		pass

	@abstractmethod
	def visit_binary_expr(self, expr):
		pass

	@abstractmethod
	def visit_grouping_expr(self, expr):
		pass

	@abstractmethod
	def visit_literal_expr(self, expr):
		pass

	@abstractmethod
	def visit_unary_expr(self, expr):
		pass

	@abstractmethod
	def visit_variable_expr(self, expr):
		pass

	@abstractmethod
	def visit_expression_stmt(self, expr):
		pass

	@abstractmethod
	def visit_print_stmt(self, expr):
		pass

	@abstractmethod
	def visit_var_stmt(self, expr):
		pass

