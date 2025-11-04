# the interpreter for the mathlang language

from mathlang.parser import Parser, parse_file, VARIABLES

class Interpreter:
    def __init__(self):
        self.variables = None
    
    def initialize_variables(self):
        self.variables = {var: 0 for var in VARIABLES}

    def interpret_code(self, code: list):  # code is a list of (left, right) tuples
        for left, right in code:
            if right.type == "literal":
                self.variables[left.var_name] = right.data[0]
            elif right.type == "variable":
                self.variables[left.var_name] = self.variables[right.data[0]]
            elif right.type == "arithmetic":
                op, left_expr, right_expr = right.data
                left_value = self.variables[left_expr.data[0]] if left_expr.type == "variable" else left_expr.data[0]
                right_value = self.variables[right_expr.data[0]] if right_expr.type == "variable" else right_expr.data[0]

                if op == "+":
                    self.variables[left.var_name] = left_value + right_value
                elif op == "-":
                    self.variables[left.var_name] = left_value - right_value
                elif op == "*":
                    self.variables[left.var_name] = left_value * right_value
                elif op == "/":
                    self.variables[left.var_name] = left_value // right_value  # integer division
                else:
                    raise ValueError(f"Unsupported operator: {op}")
    
    def print_state(self):
        if self.variables is None:
            print("Variables not initialized.")
            return
        # print the results
        for variable_name in VARIABLES:
            print(f"Value in {variable_name}: {self.variables[variable_name]}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        print("Please enter the name of the source file")
        print(f"Usage: python3 {sys.argv[0]} <source_file>")
        sys.exit(1)

    src_filename = sys.argv[1]

    asm_parser = parse_file(src_filename)

    # for i, (left, right) in enumerate(asm_parser.code):
    #     print(f"{i}: \t{left} = {right}")
    
    interpreter = Interpreter()
    interpreter.initialize_variables()

    print(f"Interpreting {len(asm_parser.code)} lines of code!\n")

    interpreter.interpret_code(asm_parser.code)
    interpreter.print_state()