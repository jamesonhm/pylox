from collections import deque
from typing import Deque
from expr import Expr, Variable
from interpreter import Interpreter
from error_handler import ErrorHandler
from stmt import Block, Stmt, Var
from token import Token 
from visitor import Visitor


class Resolver(Visitor):
    def __init__(self, interpreter: Interpreter, error_handler: ErrorHandler):
        self.interpreter = interpreter
        self.scopes: Deque = deque()
        self.error_handler = error_handler


    def resolve(self, statements: list[Stmt]):
        self._resolve_statements(statements)

    def _resolve_statements(self, statements: list[Stmt]):
        for statement in statements:
            self._resolve_statement(statement)

    def _resolve_statement(self, statement: Stmt):
        statement.accept(self)

    def _resolve_expression(self, expression: Expr):
        expression.accept(self)

    def _begin_scope(self):
        self.scopes.append({})

    def _end_scope(self):
        self.scopes.pop()

    def _declare(self, name: Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
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

    def visit_var_stmt(self, stmt:Var):
        self._declare(stmt.name)
        if stmt.initializer != None:
            self._resolve_expression(stmt.initializer)
        self._define(stmt.name)
        return None

    def visit_variable_expr(self, expr: Variable):
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) is False:
            self.error_handler.token_error(expr.name, "Can't read local variable in its own initializer.")
        self._resolve_local(expr, expr.name)
        return None


