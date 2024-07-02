
class ErrorHandler:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def error(self, line: int, message: str) -> None:
        self._report(line, "", message)

    def _report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True

