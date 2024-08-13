from collections import deque
from enum import Enum, auto
from typing import Deque
from expr import (
    Assign, 
    Binary, 
    Call, 
    Expr, 
    Grouping, 
    Literal, 
    Logical, 
    Unary, 
    Variable,
    Get,
    Set,
    This
)
from stmt import (
    Block, 
    Expression, 
    Function, 
    If, 
    Print, 
    Return, 
    Stmt, 
    Var, 
    While,
    Class
)

from interpreter import Interpreter
from error_handler import ErrorHandler
from token import Token 
from visitor import Visitor

class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    INITIALIZER = auto()
    METHOD = auto()

class ClassType(Enum):
    NONE = auto()
    CLASS = auto()


class Resolver(Visitor):
    def __init__(self, interpreter: Interpreter, error_handler: ErrorHandler):
        self.interpreter = interpreter
        self.scopes: Deque = deque()
        self.error_handler = error_handler
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def resolve(self, statements: list[Stmt]):
        self._resolve_statements(statements)

    def _resolve_statements(self, statements: list[Stmt]):
        for statement in statements:
            self._resolve_statement(statement)

    def _resolve_statement(self, statement: Stmt):
        statement.accept(self)

    def _resolve_expression(self, expression: Expr):
        expression.accept(self)

    def _resolve_local(self, expr: Expr, name: Token):
        for i, scope in enumerate(list(reversed(self.scopes))):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, i)
                return
        # if not found in any scopes, assume global and don't resolve

    def _resolve_function(self, function: Function, func_type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = func_type
        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)
        self.resolve(function.body)
        self._end_scope()
        self.current_function = enclosing_function

    def _begin_scope(self):
        self.scopes.append({})

    def _end_scope(self):
        self.scopes.pop()

    def _declare(self, name: Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.error_handler.token_error(name, "Already a variable with this name in scope.")
        scope[name.lexeme] = False

    def _define(self, name: Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def visit_block_stmt(self, stmt: Block):
        self._begin_scope()
        self.resolve(stmt.statements)
        self._end_scope()
        return None

    def visit_class_stmt(self, stmt: Class):
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS
        self._declare(stmt.name)
        self._define(stmt.name)

        self._begin_scope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = FunctionType.METHOD 
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            self._resolve_function(method, declaration)

        self._end_scope()
        self.current_class = enclosing_class
        return None

    def visit_expression_stmt(self, stmt: Expression):
        self._resolve_expression(stmt.expression)
        return None

    def visit_function_stmt(self, stmt: Function):
        self._declare(stmt.name)
        self._define(stmt.name)

        self._resolve_function(stmt, FunctionType.FUNCTION)
        return None

    def visit_if_stmt(self, stmt: If):
        self._resolve_expression(stmt.condition)
        self._resolve_statement(stmt.then_branch)
        if stmt.else_branch is not None:
            self._resolve_statement(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt: Print):
        self._resolve_expression(stmt.expression)
        return None

    def visit_return_stmt(self, stmt: Return):
        if self.current_function == FunctionType.NONE:
            self.error_handler.token_error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
            if self.current_function == FunctionType.INITIALIZER:
                self.error_handler.token_error(stmt.keyword, "Can't return a value from an initializer.")
            self._resolve_expression(stmt.value)
        return None

    def visit_var_stmt(self, stmt:Var):
        self._declare(stmt.name)
        if stmt.initializer != None:
            self._resolve_expression(stmt.initializer)
        self._define(stmt.name)
        return None

    def visit_while_stmt(self, stmt: While):
        self._resolve_expression(stmt.condition)
        self._resolve_statement(stmt.body)
        return None

    def visit_assign_expr(self, expr: Assign):
        self._resolve_expression(expr.value)
        self._resolve_local(expr, expr.name)
        return None

    def visit_binary_expr(self, expr: Binary):
        self._resolve_expression(expr.left)
        self._resolve_expression(expr.right)
        return None

    def visit_call_expr(self, expr: Call):
        self._resolve_expression(expr.callee)

        for argument in expr.arguments:
            self._resolve_expression(argument)

        return None

    def visit_get_expr(self, expr: Get):
        self._resolve_expression(expr.obj)
        return None

    def visit_grouping_expr(self, expr: Grouping):
        self._resolve_expression(expr.expression)
        return None

    def visit_literal_expr(self, expr: Literal):
        return None

    def visit_logical_expr(self, expr: Logical):
        self._resolve_expression(expr.left)
        self._resolve_expression(expr.right)
        return None

    def visit_set_expr(self, expr: Set):
        self._resolve_expression(expr.value)
        self._resolve_expression(expr.obj)

    def visit_this_expr(self, expr: This):
        if self.current_class == ClassType.NONE:
            self.error_handler.token_error(expr.keyword, "Can't use 'this' outside of a class.")
            return None
        self._resolve_local(expr, expr.keyword)
        return None

    def visit_unary_expr(self, expr: Unary):
        self._resolve_expression(expr.right)
        return None

    def visit_variable_expr(self, expr: Variable):
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) is False:
            self.error_handler.token_error(expr.name, "Can't read local variable in its own initializer.")
        self._resolve_local(expr, expr.name)
        return None


