import sys

from ast_printer import AstPrinter
from error_handler import ErrorHandler
from interpreter import Interpreter
from parser import Parser
from scanner import Scanner
from resolver import Resolver


class Lox:
    def __init__(self):
        self.interpreter = Interpreter()
        self.error_handler = ErrorHandler()

    def run_file(self, path: str) -> None:
        with open(path, 'r') as f:
            content = f.read()
            self.run(content)
            if self.error_handler.had_error:
                sys.exit(65)
            if self.error_handler.had_runtime_error:
                sys.exit(70)

    def run_prompt(self) -> None:
        try:
            print("############# PYLOX Interactive #############")
            while True:
                self.run(input(">>> "))
                self.error_handler.had_error = False
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")

    def run(self, source: str) -> None:
        scanner = Scanner(source, self.error_handler)
        tokens = scanner.scan_tokens()
        # print(f"Tokens from Scanner: {tokens}")

        parser = Parser(tokens, self.error_handler)
        statements = parser.parse()
        
        if self.error_handler.had_error:
            return

        resolver = Resolver(self.interpreter, self.error_handler)
        resolver.resolve(statements)

        if self.error_handler.had_error:
            return
        
        self.interpreter.interpret(statements)


if __name__ == "__main__":
    lox = Lox()
    if len(sys.argv[1:]) > 1:
        print(f"Usage: pylox [script]")
        sys.exit(64)
    elif len(sys.argv[1:]) == 1:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()

