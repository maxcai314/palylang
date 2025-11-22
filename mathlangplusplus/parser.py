from mathlangplusplus.expression_parser import *
from mathlangplusplus.lexer import *

class Code:
    def __init__(self):
        self.lines = []  # list of (VariableToken, Node/Token) tuples

# parser
class Parser:
    def __init__(self):
        self.code = Code()

    def parse_line(self, line: list):
        if len(line) == 0:
            return #lol
        if len(line) <= 2:
            raise ValueError("Too few tokens in line")

        lhs, assignment, *expr = line

        if not isinstance(lhs, VariableToken):
            raise ValueError("No variable to assign to")

        if not isinstance(assignment, AssignmentToken):
            raise ValueError("No assignment token")

        unresolved = UnresolvedNode.parse_parentheses(expr)
        unresolved.rewrite_depth_first(substitute_multiplication_division)
        unresolved.rewrite_depth_first(substitute_addition_subtraction)

        rhs = unresolved.unwrap()

        self.code.lines.append((lhs, rhs))


    def parse_code(self, code_tokens: list):
        start = 0
        for i in range(len(code_tokens)):
            if isinstance(code_tokens[i], NewlineToken):
                self.parse_line(code_tokens[start:i])
                start = i+1

def parse_file(src_filename: str) -> Code:
    tokens = lex_file(src_filename)
    parser = Parser()
    parser.parse_code(tokens)
    return parser.code

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Please enter the name of the source file")
        print(f"Usage: python3 {sys.argv[0]} <source_file>")
        sys.exit(1)
    
    src_filename = sys.argv[1]
    code = parse_file(src_filename)
    print(f"Parsed {len(code.lines)} lines of code.")

    for lhs, rhs in code.lines:
        print(f"{lhs.data()} = {format_tree(rhs)}")
