from error_handler import ErrorHandler
from token import Token
from tokentype import TokenType


class Scanner:
    _KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }

    def __init__(self, source: str, error_handler: ErrorHandler):
        self.source = source
        self.error_handler = error_handler
        self._tokens = []
        self._start: int = 0
        self._current: int = 0
        self._line: int = 1


    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens

    def _scan_token(self):
        c = self._advance()
        match c:
            case '(':
                self._add_token(TokenType.LEFT_PAREN)
            case ')':
                self._add_token(TokenType.RIGHT_PAREN)
            case '{':
                self._add_token(TokenType.LEFT_BRACE)
            case '}':
                self._add_token(TokenType.RIGHT_BRACE)
            case ',':
                self._add_token(TokenType.COMMA)
            case '.':
                self._add_token(TokenType.DOT)
            case '-':
                self._add_token(TokenType.MINUS)
            case '+':
                self._add_token(TokenType.PLUS)
            case ';':
                self._add_token(TokenType.SEMICOLON)
            case '*':
                self._add_token(TokenType.STAR)
            case '!':
                self._add_token(TokenType.BANG_EQUAL) if self._match('=') else self._add_token(TokenType.BANG)
            case '=':
                self._add_token(TokenType.EQUAL_EQUAL) if self._match('=') else self._add_token(TokenType.EQUAL)
            case '<':
                self._add_token(TokenType.LESS_EQUAL) if self._match('=') else self._add_token(TokenType.LESS)
            case '>':
                self._add_token(TokenType.GREATER_EQUAL) if self._match('=') else self._add_token(TokenType.GREATER)
            case '/':
                if self._match('/'):
                    while self._peek() != '\n' and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self._line += 1
            case '"':
                self._string()
            case _:
                if self._is_digit(c):
                    self._number()
                elif self._is_alpha(c):
                    self._identifier()
                else:
                    self.error_handler.scanner_error(self._line, self._current, "Unexpected character.")

    def _is_at_end(self) -> bool:
        return (self._current >= len(self.source))

    def _is_digit(self, c) -> bool:
        return c >= '0' and c <= '9'

    def _is_alpha(self, c) -> bool:
        return (c >= 'a' and c <= 'z') or\
                (c >= 'A' and c <= 'Z') or\
                (c == '_')

    def _is_alphanumeric(self, c) -> bool:
        return self._is_alpha(c) or self._is_digit(c)

    '''
    input
    '''
    def _advance(self):
        self._current += 1
        return self.source[self._current - 1]

    def _match(self, expected:str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self._current] != expected:
            return False
        self._current += 1
        return True

    def _peek(self):
        if self._is_at_end():
            return '\0'
        return self.source[self._current]

    def _peek_next(self):
        if self._current + 1 >= len(self.source):
            return '\0'
        return self.source[self._current + 1]

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == '/n':
                self._line += 1
            self._advance()

        if self._is_at_end():
            self.error_handler.error(self._line, "Unterminated String.")
            return 
        # consume closing "
        self._advance()

        value = self.source[self._start + 1:self._current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self):
        while self._is_digit(self._peek()):
            self._advance()
        if self._peek() == '.' and self._is_digit(self._peek_next()):
            self._advance()
            while self._is_digit(self._peek()):
                self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self._start:self._current]))

    def _identifier(self):
        while self._is_alphanumeric(self._peek()):
            self._advance()
        text = self.source[self._start:self._current]
        token_type = Scanner._KEYWORDS.get(text, None)
        if token_type is None:
            token_type = TokenType.IDENTIFIER
        self._add_token(token_type)


    '''
    output
    '''
    def _add_token(self, token_type: TokenType, literal=None):
        text = self.source[self._start: self._current]
        self._tokens.append(Token(token_type, text, literal, self._line))


