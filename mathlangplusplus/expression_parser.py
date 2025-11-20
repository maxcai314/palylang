# The expression parser for the mathlang++ language

from mathlangplusplus.lexer import *

# A expression contains a list of tokens which does not contain equals or newlines
class TokenExpression:
    def __init__(self, tokens: list):
        self.tokens = tokens
    
    def validate(self):
        for token in self.tokens:
            if isinstance(token, (AssignmentToken, NewlineToken)):
                raise ValueError(f"Invalid token in expression: {token}")
    
    def __repr__(self):
        return f"Expression({self.tokens})"

# Parse a TokenExpression into a abstract syntax tree
class UnresolvedNode:
    def __init__(self, tokens: list):
        """Not quite a standalone AST node yet; a string of nodes or tokens to be further parsed"""
        self.tokens = tokens
    
    def is_singular(self) -> bool:
        """Check if this UnresolvedNode contains a single token or node"""
        return len(self.tokens) == 1
    
    def unwrap(self):
        """If this UnresolvedNode contains a single token or node, return it; else raise an error"""
        if self.is_singular():
            return self.tokens[0]
        else:
            raise ValueError(f"Cannot unwrap UnresolvedNode with multiple tokens/nodes: length {len(self.tokens)}")
    
    @classmethod
    def parse_parentheses_inner(cls, token_source: iter, opened: bool = False):
        """Helper function to parse tokens with parentheses into nested UnresolvedNodes"""
        tokens = []
        
        for token in token_source:
            if isinstance(token, OpenParenToken):
                # Start a new nested UnresolvedNode
                nested_node = cls.parse_parentheses_inner(token_source, opened=True)
                tokens.append(nested_node)
            elif isinstance(token, CloseParenToken):
                if not opened:
                    raise ValueError("Mismatched closing parenthesis")
                # End of current nested UnresolvedNode
                return UnresolvedNode(tokens)
            else:
                tokens.append(token)
        
        if opened:
            raise ValueError("Mismatched opening parenthesis")
        
        return UnresolvedNode(tokens)

    @classmethod
    def parse_parentheses(cls, tokens: list):
        """Parse tokens with parentheses into nested UnresolvedNodes"""
        return cls.parse_parentheses_inner(iter(tokens), opened=False)
    
    def __repr__(self):
        return format_unresolved(self, indent=0, indent_string="  ")

def format_unresolved(node, indent=0, indent_string="|   ") -> str:
    result = ""
    terminator = ",\n" if indent > 0 else ";"
    if isinstance(node, UnresolvedNode):
        result += indent_string * indent + "UnresolvedNode {\n"
        for child in node.tokens:
            result += format_unresolved(child, indent + 1, indent_string)
        result += indent_string * indent + "}" + terminator
    else:
        result += indent_string * indent + repr(node) + terminator
    return result


if __name__ == "__main__":
    # example expression: ((a+b)*c-d/3)*f+g
    example_expression = "((a+b)*c-d/3)*f+g"
    print("Example expression:", example_expression)
    lexer = Lexer()
    for char in example_expression:
        lexer.add_char(char)
    tokens = lexer.get_completed_tokens()
    unresolved = UnresolvedNode.parse_parentheses(tokens)
    # format the tree nicely

    print("Formatted Unresolved Tree:")
    print(format_unresolved(unresolved))
