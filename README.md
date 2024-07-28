
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

expression  -> equality;  
equality    -> comparison ( ( "!=" | "==" ) comparison )* ;  
comparison  -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;  
term        -> factor ( ( "-" | "+" ) factor )* ;  
factor      -> unary ( ( "/" | "*" ) unary )* ;  
unary       ->  ( "-" | "!" ) unary ;  
primary     ->  NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;  

NUMBER: any number literal  
STRING: any string literal

The grammar is recursive, forms a syntax tree.
The syntax tree nodes are shared between the parser where they are created and the interpreter where they are consumed.  The nodes are represented by 'dumb' classes, essentially just structs with a name and some typed fields.  There is one for each of the non-terminals in the grammar.  

### The Expression Problem

We have some types, the tree nodes, and some high level operations like interpret.  Rows are types, columns are ooperations.  
OO Language organizes these by row, easy to add new classes.  But adding new operations is difficult.
Functional languages flip that and organize by column, function per operation with pattern matching for each type.  adding new functions becomes simple but new types are difficult.

|          | interpret() | resolve() | analyze() |
| ---------|-------------|-----------|-----------|
| Binary   | ... | ... | ... |
| Grouping | ... | ... | ... |
| Literal  | ... | ... | ... |
| Unary    | ... | ... | ... |

### The Visitor Pattern

Approximates the functional style in an OOP language.  Add new columns (operations) easily.  

                class Pastry(ABC):
                    @abstractmethod
                    def accept(self, visitor: PastryVisitor);
                        pass

                class Beignet(Pastry):
                    def accept(self, visitor):
                        visitor.visit_beignet(self)

                class Cruller(Pastry):
                    def accept(self, visitor):
                        visitor.visit_cruller(self)


                class PastryVisitor:
                    '''this is just an interface'''
                    visit_beignet(beignet):
                    visit_cruller(cruller):

Each new operation that needs to be implemented on a pastry is a class that implements the Visitor interface.  it has a concrete method for each type.  
To perform the operation, 
- call the accept method, 
- pass the visitor for the operation we want to execute
- the accept method calls the appropriate visit method and passes itself

## Parsing

Convert a sequence of tokens into the syntax tree.  
- Precedence: which operator evaluated first in expression containing a mix of opers. Define a separate rule in the grammar for each precedence level. each rule only matches expr's at it's precedence level or higher.  e.g. `unary` will match `!negated` or primary like `1234`.  `term` can match `1 + 2` but also `3 * 4 / 5`  
- Associativity: which operator evaluated first in series of the same oper.  

Associativity from lowest to Highest precedence.  

| Name | Operators | Associates | 
| --- | --- | --- |
| Equality | == != | Left | 
| Comparison | > >= < <= | Left | 
| Term | - + | Left | 
| Factor | / * | Left | 
| Unary | ! - | Right | 

### Recursive Descent Parsing  
Top down parser - starts from the top or outermost grammar rule (expression).  It is a literal translation of grammar rules into imperative code. Recursive when a rule refers to itself, directly or indirectly.  

Each method for parsing a grammar rule produces a syntax tree for that rule and returns it to the caller.  Each non-terminal in the rule results in a call to that rules' method.  

|  |  |  |
| --- | --- | --- |
| Top | Equality | Lower |
| ^ | Comparison | ^ |
| Grammar | Addition | Precedence |
| v | Multiplication | v |
| Bottom | Unary | Higher |

Notable Helper Methods:
- match(token_types): check to see if the current token has any of the given types.  If yes, consumes it and returns True, if no, return false and leaves the current token.  
- check(token_type): return true if the current token is the given type.  Does not consume, only looks.  
- advance(): consumes the current token and returns it.  
- consume(token_type, error_msg): when the parser knows by syntax what token shoudl come next, it can consume it directly or error if it is not there.  

### Syntax Errors
- Given an invalid sequence of tokens, detect the errors and tell the user about the mistake.  
- Modern IDE's and editors are constantly reparsing code to syntax highlight and detect errors.  
- Avoid crashing or hanging, even while parsing incorrect code.  
- Be fast.  
- Report as many distinct errors as there are.  
- Minimize cascade errors, errors caused by the parser losing it's place from bad input.  

#### Panic Mode Error Recovery
One token does not make sense given it's current state in grammar production.  Synchronization aligns the forthcoming tokens and it's state such that the next token does not match the current rule being parsed.  Parser jumps out of current nested production to get to a grammar rule synchronization point, typically between statements.  Discards tokens until in the stream until it reaches one that can appear at that point in the rule.  This avoids cascade errors.  



### TODO:
[] Error handling seems inconsistent


