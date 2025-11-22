from mathlangplusplus.lexer import *
from mathlangplusplus.expression_parser import *
from mathlangplusplus.parser import Code, parse_file

class Compiler:
    def __init__(self, code: Code):
        self.code = code
        self.defined_variables = []  # variable must be here before use
    
    def compile(self):
        output = []
        for lhs, rhs in self.code.lines:
            self.defined_variables.append(lhs.data())
            output.extend(self.compile_line(lhs, rhs))
        return output
    
    def compile_line(self, lhs: VariableToken, rhs) -> list:
        # allocate temp variables for intermediate results
        output = []
        temp_var_count = 0
        def compile_node(node, depth=0):
            nonlocal temp_var_count
            if isinstance(node, LiteralToken):
                return str(node.numeric_value())
            elif isinstance(node, VariableToken):
                if node.data() not in self.defined_variables:
                    raise ValueError(f"Variable {node.data()} used before definition")
                return node.data()
            elif isinstance(node, BinOpNode):
                left = compile_node(node.left, depth=depth+1)
                right = compile_node(node.right, depth=depth+1)
                # if at top level, assign directly to lhs
                if depth == 0:
                    return f"{left} {node.operation.data()} {right}"
                else:
                    temp_var_count += 1
                    temp_var = f"__temp_{temp_var_count}"
                    output.append(f"{temp_var} = {left} {node.operation.data()} {right}")
                    return temp_var
            else:
                raise ValueError("Unknown node type")
        
        final_result = compile_node(rhs)
        output.append(f"{lhs.data()} = {final_result}")
        return output

def compile_file(src_filename: str) -> list:
    code = parse_file(src_filename)
    compiler = Compiler(code)
    return compiler.compile()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Please enter the name of the source file")
        print(f"Usage: python3 {sys.argv[0]} <source_file> <output_file>")
        sys.exit(1)
    
    src_filename = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else None
    compiled_output = compile_file(src_filename)
    print("Compiled Output:")
    for line in compiled_output:
        print(line)
    if output_filename:
        with open(output_filename, "w") as f:
            for line in compiled_output:
                f.write(line + "\n")