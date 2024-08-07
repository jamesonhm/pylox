from expr import (
    Assign,
    Binary,
    Call,
    Expr,
    Grouping,
    Literal,
    Unary,
    Variable,
    Logical,
    Get,
    Set
)
from lox_instance import LoxInstance
from stmt import (
    Block,
    Function,
    If,
    Return,
    Stmt,
    Expression,
    Print,
    Var,
    While,
    Class
)

from environment import Environment
from lox_class import LoxClass
from lox_function import LoxFunction
from native import Clock
from token import Token
from lox_callable import LoxCallable
from error_handler import ErrorHandler
from tokentype import TokenType
from runtime_error import LoxRuntimeError
from return_exception import LoxReturnException
from visitor import Visitor


class Interpreter(Visitor):

    def __init__(self):
        self.error_handler = ErrorHandler()
        self.globals = Environment()
        self.environment = self.globals
        self.locals = dict()

        self.globals.define("clock", Clock())

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                # print(f"executing statement {statement}")
                self._execute(statement)
        except LoxRuntimeError as e:
            self.error_handler.runtime_error(e)

    def _evaluate(self, expr: Expr):
        return expr.accept(self)

    def _execute(self, stmt):
        stmt.accept(self)

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth

    def _execute_block(self, statements: list[Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            
            for statement in statements:
                # print(f"statement: {statement}")
                self._execute(statement)
        finally:
            self.environment = previous

    def visit_block_stmt(self, stmt: Block):
        self._execute_block(stmt.statements, Environment(self.environment))
        return None

    def visit_class_stmt(self, stmt: Class):
        self.environment.define(stmt.name.lexeme, None)
        methods = dict()
        for method in stmt.methods:
            function = LoxFunction(method, self.environment)
            methods[method.name.lexeme] = function
        klass = LoxClass(stmt.name.lexeme, methods)
        self.environment.assign(stmt.name, klass)
        return None

    def visit_expression_stmt(self, stmt: Expression):
        self._evaluate(stmt.expression)
        return None

    def visit_function_stmt(self, stmt: Function):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_if_stmt(self, stmt: If):
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt: Print):
        # print(f"statement: {stmt} | expression: {stmt.expression}")
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))
        return None

    def visit_return_stmt(self, stmt:Return):
        value = None
        if stmt.value != None:
            value = self._evaluate(stmt.value)
        
        raise LoxReturnException(value)

    def visit_var_stmt(self, stmt: Var):
        value = None
        if stmt.initializer != None:
            value = self._evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_while_stmt(self, stmt: While):
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)
        return None

    def visit_assign_expr(self, expr: Assign):
        value = self._evaluate(expr.value)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

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

    def visit_call_expr(self, expr: Call):
        function = self._evaluate(expr.callee)

        if not isinstance(function, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        arguments = []
        for argument in expr.arguments:
            arguments.append(self._evaluate(argument))

        if len(arguments) != function.arity():
            raise LoxRuntimeError(expr.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")

        return function.call(self, arguments)

    def visit_get_expr(self, expr: Get):
        obj = self._evaluate(expr.obj)
        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)

        raise LoxRuntimeError(expr.name, "Only instances have properties.")

    def visit_grouping_expr(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_logical_expr(self, expr: Logical):
        left = self._evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
            else:
                if not self._is_truthy(left):
                    return left
        
        return self._evaluate(expr.right)

    def visit_set_expr(self, expr: Set):
        obj = self._evaluate(expr.obj)

        if not isinstance(obj, LoxInstance):
            raise LoxRuntimeError(expr.name, "Only instances have fields.")

        value = self._evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    def visit_unary_expr(self, expr: Unary):
        right = self._evaluate(expr.right)
        
        if expr.operator.token_type == TokenType.MINUS:
            self._check_numeric_oper(expr.operator, right)
            return -float(right)
        elif expr.operator.token_type == TokenType.BANG:
            return not self._is_truthy(right)

        # return None

    def visit_variable_expr(self, expr: Variable):
        return self._lookup_variable(expr.name, expr)

    def _lookup_variable(self, name: Token, expr: Expr):
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

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


