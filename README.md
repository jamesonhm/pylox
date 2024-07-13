
# Python implementation of the Lox Language
### From the book Crafting Interpreters by Robert Nystrom

### Note* this implementation is still incomplete

### Reference notes to remember where we've been:

# Part II Tree Walk Interpreter

## Scanning
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

## Representing Code 
* Context free grammar: uses an "alphabet" consisting of the tokens produced by the scanner and defines the set of strings possible with them.
* rules comprised of a head and a body, the head is a single symbol, the body is what it generates
* Symbols are either terminal, an individual token, or nonterminal, a reference to another rule 

### Lox's Grammar
expression  ->  literal
                | unary
                | binary
                | grouping ;

literal     ->  NUMBER | STRING | "true" | "false" | "nil" ;
grouping    ->  "(" expression ")" ;
unary       ->  ( "-" | "!" ) expression ;
binary      ->  expression operator expression ;
operator    ->  "==" | "!=" | "<" | "<=" | ">" | ">=" 
                | "+" | "-" | "*" | "/" ;

NUMBER: any number literal
STRING: any string literal

### TODO:
[] Error handling seems inconsistent


