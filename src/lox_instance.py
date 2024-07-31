from token import Token

from runtime_error import LoxRuntimeError

class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = dict()

    def get(self, name: Token):
        if name.lexeme in self.fields.keys():
            return self.fields[name.lexeme]

        raise LoxRuntimeError(name, f"Undefined property {name.lexeme}.")

    def __str__(self):
        return f"{self.klass.name} instance"
