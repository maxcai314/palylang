from mathlangplusplus.expression_parser import *
from mathlangplusplus.lexer import *

class Code:
    def __init__(self):
        self.variables = []
        self.lines = []  # list of (LeftExpr, RightExpr) tuples

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
        for i in range(len(list)):
            if isinstance(code_tokens[i], NewlineToken):
                self.parse_line(code_tokens[start:i])
                start = i+1