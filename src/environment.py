from __future__ import annotations

from typing import Any, Dict, Optional

from runtime_error import LoxRuntimeError
from token import Token 


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None):
        self.values: Dict[str, Any] = dict()
        self.enclosing = enclosing

    def define(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
            return
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
