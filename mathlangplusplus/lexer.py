# Lexes mathlang++ source code into tokens.

from abc import ABC, abstractmethod
import re

VAR_NAME_PATTERN = r"^[a-zA-Z_][a-zA-Z0-9_]*$"  # can be split into two parts
VAR_NAME_START_CHAR_PATTERN = r"[a-zA-Z_]"
VAR_NAME_REMAINDER_CHAR_PATTERN = r"[a-zA-Z0-9_]"

LITERAL_PATTERN = r"^[+\-]?\d+$"  # optional plus or minus sign followed by digits
LITERAL_START_CHAR_PATTERN = r"[+\-\d]"  # either +, -, or digit
LITERAL_REMAINDER_CHAR_PATTERN = r"\d"

OPEN_PAREN_CHAR = "("
CLOSE_PAREN_CHAR = ")"

ASSIGNMENT_CHAR = "="
ARITHMETIC_OPERATORS = { "+", "-", "*", "/" }
NEWLINE_CHAR = "\n"
SPACERS = { " ", "\t", "\r" }
COMMENT_START = "#"

# token types (lexemes): variable, literal, operator, assignment, newline, open_paren, close_paren
class Token(ABC):
    @abstractmethod
    def data(self) -> str:
        pass
    @abstractmethod
    def validate(self) -> None:
        pass
    @abstractmethod
    def __repr__(self):
        pass

class VariableToken(Token):
    def __init__(self, name: str):
        self.name = name
    
    def data(self) -> str:
        return self.name
    
    def validate(self) -> None:
        if not re.match(VAR_NAME_PATTERN, self.name):
            raise ValueError(f"Invalid variable name: {self.name}")

    def __repr__(self):
        return f"VariableToken({self.name})"

class LiteralToken(Token):
    def __init__(self, str_value: str):
        self.str_value = str_value
    
    def data(self) -> str:
        return self.str_value
    
    def numeric_value(self) -> int:
        return int(self.str_value)
    
    def validate(self) -> None:
        if not re.match(LITERAL_PATTERN, self.str_value):
            raise ValueError(f"Invalid literal value: {self.str_value}")
    
    def __repr__(self):
        return f"LiteralToken({self.str_value})"

class OperatorToken(Token):
    def __init__(self, operator: str):
        self.operator = operator
    
    def data(self) -> str:
        return self.operator
    
    def validate(self) -> None:
        if self.operator not in ARITHMETIC_OPERATORS:
            raise ValueError(f"Invalid operator: {self.operator}")
    
    def __repr__(self):
        return f"OperatorToken({self.operator})"

class AssignmentToken(Token):
    def data(self) -> str:
        return ASSIGNMENT_CHAR
    
    def validate(self) -> None:
        pass  # always valid
    
    def __repr__(self):
        return f"AssignmentToken({ASSIGNMENT_CHAR})"

class NewlineToken(Token):
    def data(self) -> str:
        return NEWLINE_CHAR
    
    def validate(self) -> None:
        pass  # always valid
    
    def __repr__(self):
        return "NewlineToken(\\n)"

class OpenParenToken(Token):
    def data(self) -> str:
        return OPEN_PAREN_CHAR
    
    def validate(self) -> None:
        pass  # always valid
    
    def __repr__(self):
        return f"OpenParenToken({OPEN_PAREN_CHAR})"

class CloseParenToken(Token):
    def data(self) -> str:
        return CLOSE_PAREN_CHAR
    
    def validate(self) -> None:
        pass  # always valid
    
    def __repr__(self):
        return f"CloseParenToken({CLOSE_PAREN_CHAR})"


# Lexer accepts characters one at a time and pushes tokens
class Lexer:
    def __init__(self):
        self.tokens = []
        self.current_lexeme = None  # current lexeme being built
        self.is_in_comment = False
    
    def finalize(self):
        if self.current_lexeme is not None:
            self.tokens.append(self.current_lexeme)
            self.current_lexeme = None
    
    def add_initial_char(self, char: str):
        if self.current_lexeme is not None:
            raise ValueError(f"Current lexeme already in progress: {self.current_lexeme}")
        if self.is_in_comment:
            # the only thing that ends a comment is a newline
            if char == NEWLINE_CHAR:
                self.tokens.append(NewlineToken())
                self.is_in_comment = False
                self.current_lexeme = None
            return
            # ignore characters in comment
        # determine type of lexeme
        if re.match(VAR_NAME_START_CHAR_PATTERN, char):
            self.current_lexeme = VariableToken(char)
        elif re.match(LITERAL_START_CHAR_PATTERN, char):
            self.current_lexeme = LiteralToken(char)
        elif char in ARITHMETIC_OPERATORS:
            self.tokens.append(OperatorToken(char))
            self.current_lexeme = None  # no lexeme in progress
        elif char == ASSIGNMENT_CHAR:
            self.tokens.append(AssignmentToken())
            self.current_lexeme = None  # no lexeme in progress
        elif char == NEWLINE_CHAR:
            self.tokens.append(NewlineToken())
            self.current_lexeme = None  # no lexeme in progress
        elif char == COMMENT_START:
            self.is_in_comment = True
            self.current_lexeme = None  # no lexeme in progress
        elif char == OPEN_PAREN_CHAR:
            self.tokens.append(OpenParenToken())
            self.current_lexeme = None  # no lexeme in progress
        elif char == CLOSE_PAREN_CHAR:
            self.tokens.append(CloseParenToken())
            self.current_lexeme = None  # no lexeme in progress
        elif char in SPACERS:
            pass  # ignore spacers
        else:
            raise ValueError(f"Invalid character: {char}")

    def add_char(self, char: str):
        if self.current_lexeme is None:
            self.add_initial_char(char)
        else:
            # greedy algorithm:
            # attempt to continue current lexeme
            if isinstance(self.current_lexeme, VariableToken):
                if re.match(VAR_NAME_REMAINDER_CHAR_PATTERN, char):
                    self.current_lexeme.name += char
                else:
                    # finalize current lexeme and start new one
                    self.finalize()
                    self.add_initial_char(char)
            elif isinstance(self.current_lexeme, LiteralToken):
                if re.match(LITERAL_REMAINDER_CHAR_PATTERN, char):
                    self.current_lexeme.str_value += char
                else:
                    # if the only char was + or -, then it's actually an operator
                    if self.current_lexeme.str_value in { "+", "-" }:
                        # switch to operator instead
                        self.current_lexeme = OperatorToken(self.current_lexeme.str_value)
                    # finalize current lexeme and start new one
                    self.finalize()
                    self.add_initial_char(char)
            else:
                raise ValueError(f"Current lexeme is not extendable: {self.current_lexeme}")
    
    def compact(self):
        # eliminate doubled newlines
        compacted_tokens = []
        prev_was_newline = True  # newline at start is unnecessary
        for token in self.tokens:
            if isinstance(token, NewlineToken):
                if not prev_was_newline:
                    compacted_tokens.append(token)
                    prev_was_newline = True
            else:
                compacted_tokens.append(token)
                prev_was_newline = False
        self.tokens = compacted_tokens
    
    def get_completed_tokens(self) -> list:
        self.finalize()
        self.compact()
        return list(self.tokens)


def lex_file(src_filename: str) -> list:
    # return token list
    lexer = Lexer()
    with open(src_filename, "r") as f:
        while True:
            char = f.read(1)
            if not char:
                break
            lexer.add_char(char)
    lexer.add_char(NEWLINE_CHAR)  # ensure final newline
    return lexer.get_completed_tokens()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Please enter the name of the source file")
        print(f"Usage: python3 {sys.argv[0]} <source_file>")
        sys.exit(1)
    
    src_filename = sys.argv[1]
    tokens = lex_file(src_filename)
    print("Reconstructed code:")
    for token in tokens:
        if isinstance(token, NewlineToken):
            print()
        else:
            print(token.data(), end=" ")
    print(f"Lexed {len(tokens)} tokens.")

    # ANSI color codes for terminal output
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    END = "\033[0m"

    print()
    print(f"{BLUE}Variable{END} {GREEN}Literal{END} {RED}Operator{END} {YELLOW}Assignment{END} {PURPLE}Newline{END} {CYAN}Parentheses{END}")
    print("Colored Tokens:\n")

    # print colored tokens
    for token in tokens:
        text = token.data()
        if isinstance(token, VariableToken):
            color = BLUE
        elif isinstance(token, LiteralToken):
            color = GREEN
        elif isinstance(token, OperatorToken):
            color = RED
        elif isinstance(token, AssignmentToken):
            color = YELLOW
        elif isinstance(token, NewlineToken):
            color = PURPLE
            text = "\\n"
        elif isinstance(token, OpenParenToken) or isinstance(token, CloseParenToken):
            color = CYAN
        else:
            color = END
        print(f"{color}{text}{END}", end=" ")
        if isinstance(token, NewlineToken):
            print()
    print()

    # print("Tokens:")
    # print(tokens)

