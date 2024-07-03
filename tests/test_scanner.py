import pytest 

from src.error_handler import ErrorHandler
from src.scanner import Scanner
from src.token import Token
from src.tokentype import TokenType

source_inputs = [
    "var name = 12"
]
token_inputs = [
    [Token(TokenType.VAR, "", None, 0), 
     Token(TokenType.IDENTIFIER, "", None, 0),
     Token(TokenType.EQUAL, "", None, 0),
     Token(TokenType.NUMBER, "", 12, 0)
     ]
]

@pytest.mark.parametrize("source,expected_tokens", list(zip(source_inputs, token_inputs)))
def test_scanner(source, expected_tokens):
    error_handler = ErrorHandler()
    scanner = Scanner(source, error_handler)
    assert scanner.scan_tokens() == expected_tokens

