from runtime_error import LoxRuntimeError

class LoxReturnException(LoxRuntimeError):
    """
    This is a hack to return values from lox functions
    """

    def __init__(self, value):
        super().__init__(None, None)
        self.value = value

