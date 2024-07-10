
# Python implementation of the Lox Language
### From the book Crafting Interpreters by Robert Nystrom

### Note* this implementation is still incomplete

### Reference notes to remember where we've been:

# Part II Tree Walk Interpreter

## Chapter 4 Scanning
(Also know as Lexing or Tokenizing)

### Interpreter Framework
* Define Token Types, this is just an enum here, with one name for each unique type of token
* Define the Token data structure
a. TokenType
b. lexeme (string representation of the character(s))
c. literal
d. line (source file line number where the token is found)
* Iterate over each character in the source code text to find meaningful 'chunks' called tokens
a. start and current fields index into the source to track the length of tokens
b. single character tokens are found simply with a switch or if/else
c. whitespace is skipped
d. start of a string literal is id'd by a quote " or '
e. start of numeric literal id'd by is_digit
f. assume any lexeme starting with a letter or underscore is an identifier, then check it agains teh list of reserved/key words


### TODO:
[ ] Error handling seems inconsistent


