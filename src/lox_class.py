
from typing import Any
from lox_callable import LoxCallable
from lox_instance import LoxInstance
from lox_function import LoxFunction


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: dict):
        self.name = name
        self.methods = methods

    def __str__(self):
        return self.name

    def call(self, interpreter, arguments: list[Any]):
        instance = LoxInstance(self)
        initializer: LoxFunction = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self) -> int:
        initializer: LoxFunction = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def find_method(self, name: str):
        if name in self.methods.keys():
            return self.methods[name]
        return None
