# The parser for the mathlang language

"""
Here are the rules of my simple language:
There are only three predefined variables: a, b, c
A line of code may contain a statement and/or a comment
There is only one type of statement: assignment
<lhs> = <rhs>
The left-hand side of assignment must be a variable name
The right-hand side is an expression
Expressions are either arithmetic operations, variable names, or literal numbers
The two sides of an arithmetic operation can be a variable name or a literal
+, -, *, /
a = 15 - a  # lol
"""

VARIABLES = [ "a", "b", "c" ]

def trim_line(line):
    # remove comments
    comment_start = line.find("#")
    if comment_start != -1:
        line = line[:comment_start]

    # remove leading and trailing whitespace
    line = line.strip()

    return line

class LeftExpr:
    """
    Left-hand side expression - must be a variable name
    """
    def __init__(self, var_name):
        if var_name not in VARIABLES:
            raise ValueError(f"Invalid lhs variable name: {var_name}")
        self.var_name = var_name

    def validate(self):
        if self.var_name not in VARIABLES:
            raise ValueError(f"Invalid lhs variable name: {self.var_name}")
    
    def __repr__(self):
        return f"LeftExpr({self.var_name})"

RIGHT_EXPR_TYPES = [ "literal", "variable", "arithmetic" ]
ARITHMETIC_OPERATORS = [ "+", "-", "*", "/" ]

class RightExpr:
    """
    Right-hand side expression - can be a variable name, literal, or arithmetic expression
    """
    def __init__(self, type: str, data: list):
        if type not in RIGHT_EXPR_TYPES:
            raise ValueError(f"Invalid right expression type: {type}")
        self.type = type
        self.data = data
    
    def validate(self):
        if self.type == "literal":
            if len(self.data) != 1 or not isinstance(self.data[0], int):
                raise ValueError("Literal right expression must contain one integer value")
        elif self.type == "variable":
            if len(self.data) != 1 or self.data[0] not in VARIABLES:
                raise ValueError("Variable right expression must contain one valid variable name")
        elif self.type == "arithmetic":
            if len(self.data) != 3:
                raise ValueError("Arithmetic right expression must contain operator and two operands")
            op, left, right = self.data
            if op not in ARITHMETIC_OPERATORS:
                raise ValueError(f"Invalid arithmetic operator: {op}")
            if not isinstance(left, RightExpr) or not isinstance(right, RightExpr):
                raise ValueError("Operands of arithmetic expression must be RightExpr instances")
            left.validate()
            right.validate()
    
    def __repr__(self):
        return f"RightExpr({self.type}, {self.data})"

# since each line of code is independent, we can lex and parse in one pass
class Parser:
    def __init__(self):
        self.code = []  # list of (left, right) tuples
    
    def parse_line(self, line: str):
        line = trim_line(line)

        if len(line) == 0:
            return  # skip empty lines

        # split by equals sign
        if "=" not in line:
            raise ValueError(f"Invalid statement (no '='): {line}")
        lhs, rhs = line.split("=", 1)
        lhs = lhs.strip()
        rhs = rhs.strip()

        left_expr = LeftExpr(lhs)
        right_expr = self.parse_right_expr(rhs)

        self.code.append((left_expr, right_expr))
    
    def parse_primitive(self, token: str):
        # check if it's a variable
        if token in VARIABLES:
            return RightExpr("variable", [token])
        
        # check if it's a literal number
        try:
            value = int(token)
            return RightExpr("literal", [value])
        except ValueError:
            pass

        return None
    
    def parse_right_expr(self, expr: str) -> RightExpr:
        # check if it's a primitive
        primitive = self.parse_primitive(expr)
        if primitive is not None:
            return primitive

        # check if it's an arithmetic expression
        for op in ARITHMETIC_OPERATORS:
            if op in expr:
                left, right = expr.split(op, 1)
                left = left.strip()
                right = right.strip()
                left_primitive = self.parse_primitive(left)
                right_primitive = self.parse_primitive(right)
                if left_primitive is None or right_primitive is None:
                    raise ValueError(f"Invalid operands in arithmetic expression: {expr}")
                return RightExpr("arithmetic", [op, left_primitive, right_primitive])
        else:
            raise ValueError(f"Invalid right-hand side expression: {expr}")
    
    def validate(self):
        for left, right in self.code:
            if not isinstance(left, LeftExpr) or not isinstance(right, RightExpr):
                raise ValueError("Code line does not contain valid LeftExpr and RightExpr")
            left.validate()
            right.validate()


def parse_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    parser = Parser()
    for line in lines:
        parser.parse_line(line)
    parser.validate()

    return parser


if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        print("Please enter the name of the source file")
        print(f"Usage: python3 {sys.argv[0]} <source_file>")
        sys.exit(1)

    src_filename = sys.argv[1]

    asm_parser = parse_file(src_filename)

    for i, (left, right) in enumerate(asm_parser.code):
        print(f"{i}: \t{left} = {right}")
