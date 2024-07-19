from environment import Environment
from lox_callable import LoxCallable
from stmt import Function


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for param, arg in list(zip(self.declaration.params, arguments)):
            environment.define(param.lexeme, arg)

        interpreter._execute_block(self.declaration.body, environment)
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

