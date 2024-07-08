import sys

from scanner import Scanner
from error_handler import ErrorHandler
from ast_printer import AstPrinter
from parser import Parser
from token import Token


class Lox:
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler

    def run_file(self, path: str) -> None:
        with open(path, 'r') as f:
            content = f.read()
            self.run(content)
            if self.error_handler.had_error:
                sys.exit(65)

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
        print(f"Tokens from Scanner: {tokens}")

        parser = Parser(tokens, self.error_handler)

        expression = parser.parse()
        
        if self.error_handler.had_error:
            return
        
        if expression is not None:
            print(AstPrinter().print_ast(expression))

if __name__ == "__main__":
    error_handler = ErrorHandler()
    lox = Lox(error_handler)
    if len(sys.argv[1:]) > 1:
        print(f"Usage: pylox [script]")
        sys.exit(64)
    elif len(sys.argv[1:]) == 1:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()

