import time
from lox_callable import LoxCallable


class Clock(LoxCallable):
    def call(self, interpreter, arguments):
        return time.time()

    def arity(self) -> int:
        return 0

    def __str__(self):
        return "<native fn>"

