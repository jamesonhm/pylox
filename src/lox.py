import sys

class Lox:
    def __init__(self):
        self.had_error: bool = False

    def run_file(self, path: str) -> None:
        with open(path, 'r') as f:
            content = f.read()
            self.run(content)
            if self.had_error:
                sys.exit(65)

    def run_prompt(self) -> None:
        try:
            print("############# PYLOX Interactive #############")
            while True:
                self.run(input(">>> "))
                self.had_error = False
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")

    def run(self, source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def error(self, line: int, message: str) -> None:
        self._report(line, "", message)

    def _report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True


if __name__ == "__main__":
    lox = Lox()
    if len(sys.argv[1:]) > 1:
        print(f"Usage: pylox [script]")
        sys.exit(64)
    elif len(sys.argv[1:]) == 1:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()

