
from expr import Binary, Expr, Grouping, Literal, Unary
from token import Token
from tokentype import TokenType
from visitor import Visitor


class AstPrinter(Visitor):

    def print_ast(self, expr: Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary):
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def visit_expression_stmt(self):
        pass

    def _parenthesize(self, name: str, *args: Expr):
        builder = ["(", name]   
        for expr in args:
            if expr is not None:
                builder.append(' ')
                builder.append(expr.accept(self))
        builder.append(")")
        return ''.join(builder)

def main():
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )
    print(AstPrinter().print_ast(expression))

if __name__ == "__main__":
    main()

