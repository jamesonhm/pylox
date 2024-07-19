from token import Token 
from tokentype import TokenType

class ErrorHandler:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def scanner_error(self, line: int, column: int, message: str):
        self._report(line, f" at column {column}", message)

    def token_error(self, token: Token, message: str):
        if token.token_type == TokenType.EOF:
            self._report(token.line, " at end", message)
        else:
            self._report(token.line, " at '" + token.lexeme + "'", message)

    def runtime_error(self, error):
        print(f"[Line {error.token.line}] --> {error.message}")
        self.had_error = True
        self.had_runtime_error = True

    def _report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True

