# The expression parser for the mathlang++ language

from mathlangplusplus.lexer import *
from abc import ABC, abstractmethod

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

class Node(ABC):
    @abstractmethod
    def rewrite_depth_first(self, rewrite_function):
        """
        Apply a rewrite function to all UnresolvedNodes in this expression tree in depth-first order.
        The rewrite_function should take a list of tokens/nodes and return a new list of tokens/nodes,
        emulating a transformation for each token string in the expression tree.
        This modifies the tree in place.
        """
        pass
    @abstractmethod
    def unwrap(self):
        """
        Recursively unwrap all UnresolvedNodes that contain a single token or node,
        replacing them with their contained token/node.
        Returns the unwrapped node.
        """
        pass
    @abstractmethod
    def __repr__(self):
        pass

# Parse a TokenExpression into a abstract syntax tree
class UnresolvedNode(Node):
    def __init__(self, tokens: list):
        """Not quite a standalone AST node yet; a string of nodes or tokens to be further parsed"""
        self.tokens = tokens
    
    def is_singular(self) -> bool:
        """Check if this UnresolvedNode contains a single token or node"""
        return len(self.tokens) == 1
    
    def unwrap(self):
        """If this UnresolvedNode contains a single token or node, return it; else raise an error"""
        if self.is_singular():
            result = self.tokens[0]
            if isinstance(result, Node):
                return result.unwrap()
            else:
                return result
        else:
            raise ValueError(f"Cannot unwrap UnresolvedNode with multiple tokens/nodes: length {len(self.tokens)}")
    
    def rewrite_depth_first(self, rewrite_function):
        # First, recursively apply the rewrite function to all child UnresolvedNodes
        new_tokens = []
        for token in self.tokens:
            if isinstance(token, Node):
                token.rewrite_depth_first(rewrite_function)
                new_tokens.append(token)
            else:
                new_tokens.append(token)
        # Finally, apply the rewrite function to this node
        self.tokens = list(rewrite_function(new_tokens))
    
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
        return format_tree(self, indent=0, indent_string="", separator=" ")

class BinOpNode(Node):
    def __init__(self, operation: OperatorToken, left, right):
        """Resolved Node with an operation, left value, and right value"""
        self.operation = operation
        self.left = left
        self.right = right
    
    def unwrap(self):
        # need to unwrap left and right
        if isinstance(self.left, Node):
            self.left = self.left.unwrap()
        if isinstance(self.right, Node):
            self.right = self.right.unwrap()
        return self
    
    def rewrite_depth_first(self, rewrite_function):
        # Recursively apply the rewrite function to left and right
        if isinstance(self.left, Node):
            self.left.rewrite_depth_first(rewrite_function)
        
        if isinstance(self.right, Node):
            self.right.rewrite_depth_first(rewrite_function)

    def __repr__(self):
        return f"BinOpNode({self.operation}, {self.left}, {self.right})"


def format_tree(node, indent=0, indent_string="|   ", separator="\n") -> str:
    result = ""
    terminator = "," + separator if indent > 0 else ";"
    if isinstance(node, UnresolvedNode):
        result += indent_string * indent + "UnresolvedNode {" + separator
        for child in node.tokens:
            result += format_tree(child, indent + 1, indent_string, separator)
        result += indent_string * indent + "}" + terminator
    elif isinstance(node, BinOpNode):
        result += indent_string * indent + "BinOpNode {" + separator
        result += format_tree(node.operation, indent + 1, indent_string, separator)
        result += format_tree(node.left, indent + 1, indent_string, separator)
        result += format_tree(node.right, indent + 1, indent_string, separator)
        result += indent_string * indent + "}" + terminator
    else:
        result += indent_string * indent + repr(node) + terminator
    return result


def substitute_multiplication_division(tokens: list) -> list:
    # this could be converted into an iterator/generator for future optimization
    result = []
    # state machine
    previous_token = None
    operator = None
    for token in tokens:
        if previous_token is None:
            previous_token = token
        elif operator is None:
            if isinstance(token, OperatorToken) and token.operator in ('*', '/'):
                operator = token
            else:
                # just pass through
                result.append(previous_token)
                previous_token = token
        else:
            # we have an operator and a previous token
            # prev, operator, and token form a multiplication/division operation
            bin_op_node = BinOpNode(operator, previous_token, token)
            previous_token = bin_op_node
            operator = None
    # if after done, we have a dangling operator, it's an error
    if operator is not None:
        raise ValueError(f"Dangling operator without right operand: {operator}")
    # flush remaining token
    if previous_token is not None:
        result.append(previous_token)
    return result


def substitute_addition_subtraction(tokens: list) -> list:
    raise NotImplementedError("Addition and subtraction substitution not yet implemented")
    # similar to multiplication/division, but for + and - operators

if __name__ == "__main__":
    print()
    # example expression: ((a+b)*c-d/3)*f+g
    example_expression = "a * b / c"
    print("Example expression:", example_expression)
    lexer = Lexer()
    for char in example_expression:
        lexer.add_char(char)
    tokens = lexer.get_completed_tokens()
    unresolved = UnresolvedNode.parse_parentheses(tokens)

    print("Unresolved Tree:")
    print(format_tree(unresolved))

    print("\nBinding multiplication/division:")
    unresolved.rewrite_depth_first(substitute_multiplication_division)
    print(format_tree(unresolved.unwrap()))

    print()
