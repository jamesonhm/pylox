from environment import Environment
from lox_callable import LoxCallable
from return_exception import LoxReturnException
from stmt import Function


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for param, arg in list(zip(self.declaration.params, arguments)):
            environment.define(param.lexeme, arg)

        try:
            interpreter._execute_block(self.declaration.body, environment)
        except LoxReturnException as return_value:
            return return_value.value
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

