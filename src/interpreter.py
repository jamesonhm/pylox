from expr import (
    Binary,
    Expr,
    Grouping,
    Literal,
    Unary
)
from token import Token
from error_handler import ErrorHandler 
from tokentype import TokenType
from runtime_error import LoxRuntimeError
from visitor import Visitor


class Interpreter(Visitor):

    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler

    def interpret(self, expr: Expr):
        try:
            value = self._evaluate(expr)
            print(self._stringify(value))
        except LoxRuntimeError as e:
            self.error_handler.runtime_error(e)

    def _evaluate(self, expr: Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        token_type = expr.operator.token_type
        if token_type in (
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.MINUS,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            self._check_numeric_opers(expr.operator, left, right)
        if token_type == TokenType.GREATER:
            return float(left) > float(right)
        if token_type == TokenType.GREATER_EQUAL:
            return float(left) >= float(right)
        if token_type == TokenType.LESS:
            return float(left) < float(right)
        if token_type == TokenType.LESS_EQUAL:
            return float(left) <= float(right)
        if token_type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        if token_type == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)
        if token_type == TokenType.MINUS:
            return float(left) - float(right)
        if token_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        if token_type == TokenType.SLASH:
            return float(left) / float(right)
        if token_type == TokenType.STAR:
            return float(left) * float(right)

        # return None

    def visit_grouping_expr(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        right = self._evaluate(expr.right)
        
        if expr.operator.token_type == TokenType.MINUS:
            self._check_numeric_oper(expr.operator, right)
            return -float(right)
        elif expr.operator.token_type == TokenType.BANG:
            return not self._is_truthy(right)

        # return None

    def _check_numeric_oper(self, operator: Token, right: Expr):
        if isinstance(right, (float, int)):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def _check_numeric_opers(self, operator: Token, left: Expr, right: Expr):
        if isinstance(left, (float, int)) and isinstance(right, (float, int)):
            return
        raise LoxRuntimeError(operator, "Operands must be a number.")

    def _is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def _is_equal(self, a, b):
        if a == None and b == None:
            return True
        if a == None:
            return False
        return a == b

    def _stringify(self, object):
        if object is None:
            return "nil"
        if isinstance(object, float):
            text = str(object)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(object)

    def visit_expression_stmt(self):
        pass

