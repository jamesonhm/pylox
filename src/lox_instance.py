from token import Token
from typing import Any

from runtime_error import LoxRuntimeError

class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = dict()

    def get(self, name: Token):
        if name.lexeme in self.fields.keys():
            return self.fields[name.lexeme]

        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise LoxRuntimeError(name, f"Undefined property {name.lexeme}.")

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value

    def __str__(self):
        return f"{self.klass.name} instance"
