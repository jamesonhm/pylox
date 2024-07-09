
from token import Token

from expr import Binary, Expr, Grouping, Literal, Unary
from stmt import Expression, Print, Stmt
from tokentype import TokenType
from error_handler import ErrorHandler


class ParseError(Exception):
    pass

class Parser:

    def __init__(self, tokens: list[Token], error_handler: ErrorHandler):
        self.tokens = tokens
        self.current = 0
        self.error_handler = error_handler

    def parse(self) -> list[Stmt]:
        statements = []
        while not self._is_at_end():
            statements.append(self._statement())
        return statements

    def _expression(self) -> Expr:
        return self._equality()

    def _statement(self) -> Stmt:
        if self._match(TokenType.PRINT):
            return self._print_statement()
        return self._expression_statement()

    def _print_statement(self) -> Stmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def _expression_statement(self) -> Stmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return  Expression(expr)

    def _equality(self) -> Expr:
        expr = self._comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)

        return expr

    def _comparison(self) -> Expr:
        expr = self._term()

        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)

        return expr

    def _term(self) -> Expr:
        expr = self._factor()

        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)

        return expr

    def _factor(self) -> Expr:
        expr = self._unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)

        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)
        
        return self._primary()

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)
        
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(expr)
        self.error_handler.token_error(self._peek(), "Expect Expression")

    def _match(self, *args: TokenType) -> bool:
        for t in args:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().token_type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current +=1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().token_type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _error(self, token: Token, message: str) -> ParseError:
        self.error_handler.token_error(token, message)
        raise ParseError(message)

    def _synchronize(self):
        self._advance()

        while not self._is_at_end():
            if self._previous().token_type == TokenType.SEMICOLON:
                return
            
            if self._peek().type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return
        self._advance()


