from abc import ABC, abstractmethod

class Visitor(ABC):

	@abstractmethod
	def visit_assign_expr(self, expr):
		pass

	@abstractmethod
	def visit_binary_expr(self, expr):
		pass

	@abstractmethod
	def visit_call_expr(self, expr):
		pass

	@abstractmethod
	def visit_get_expr(self, expr):
		pass

	@abstractmethod
	def visit_grouping_expr(self, expr):
		pass

	@abstractmethod
	def visit_literal_expr(self, expr):
		pass

	@abstractmethod
	def visit_logical_expr(self, expr):
		pass

	@abstractmethod
	def visit_set_expr(self, expr):
		pass

	@abstractmethod
	def visit_unary_expr(self, expr):
		pass

	@abstractmethod
	def visit_variable_expr(self, expr):
		pass

	@abstractmethod
	def visit_block_stmt(self, expr):
		pass

	@abstractmethod
	def visit_class_stmt(self, expr):
		pass

	@abstractmethod
	def visit_expression_stmt(self, expr):
		pass

	@abstractmethod
	def visit_function_stmt(self, expr):
		pass

	@abstractmethod
	def visit_if_stmt(self, expr):
		pass

	@abstractmethod
	def visit_print_stmt(self, expr):
		pass

	@abstractmethod
	def visit_return_stmt(self, expr):
		pass

	@abstractmethod
	def visit_var_stmt(self, expr):
		pass

	@abstractmethod
	def visit_while_stmt(self, expr):
		pass

