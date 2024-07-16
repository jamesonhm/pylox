from abc import ABC, abstractmethod
from typing import Any

class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments: list[Any]):
        pass

    @abstractmethod
    def arity(self) -> int:
        pass


