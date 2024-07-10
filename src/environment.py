
from typing import Any, Dict

from runtime_error import LoxRuntimeError
from token import Token 


class Environment:
    def __init__(self):
        self.values: Dict[str, Any] = dict()

    def define(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
