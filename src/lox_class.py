
from typing import Any
from lox_callable import LoxCallable
from lox_instance import LoxInstance


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: dict):
        self.name = name
        self.methods = methods

    def __str__(self):
        return self.name

    def call(self, interpreter, arguments: list[Any]):
        instance = LoxInstance(self)
        return instance

    def arity(self) -> int:
        return 0

    def find_method(self, name: str):
        if name in self.methods.keys():
            return self.methods[name]
        return None
