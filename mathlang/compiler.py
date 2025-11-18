# the compiler for the mathlang language

from mathlang.parser import Parser, Code, parse_file, LeftExpr, RightExpr


LIB_FILE = "mathlang/lib_asm.txt"

class Compiler:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.register_mappings = {
            "a": "a0",
            "b": "a1",
            "c": "a2"
        }
        self.temp_reg = "a3"  # temporary register for computations
        self.insn_mappings = {
            "+": "add",
            "-": "sub",
            "*": "mul",
            "/": "div"
        }

    def map_register(self, var_name: str) -> str:
        if var_name not in self.register_mappings:
            raise ValueError(f"Unknown variable name: {var_name}")
        return self.register_mappings[var_name]

    def target_instruction(self, operator: str) -> str:
        if operator not in self.insn_mappings:
            raise ValueError(f"Unsupported operator: {operator}")
        return self.insn_mappings[operator]
    
    def compile_statement(self, left: LeftExpr, right: RightExpr) -> list:
        asm_lines = []

        dest_reg = self.map_register(left.var_name)

        if right.type == "literal":
            value = right.data[0]
            asm_lines.append(f"  addi {dest_reg}, zero, {value}")
        elif right.type == "variable":
            src_reg = self.map_register(right.data[0])
            asm_lines.append(f"  addi {dest_reg}, {src_reg}, 0")
        elif right.type == "arithmetic":
            op, left_expr, right_expr = right.data
            target_insn = self.target_instruction(op)

            if left_expr.type == "literal" and right_expr.type == "literal":
                # strategy: if both operands are literals, load left into dest, right into temp, then operate
                left_value = left_expr.data[0]
                right_value = right_expr.data[0]
                asm_lines.append(f"  addi {dest_reg}, zero, {left_value}")
                asm_lines.append(f"  addi {self.temp_reg}, zero, {right_value}")
                asm_lines.append(f"  {target_insn} {dest_reg}, {dest_reg}, {self.temp_reg}")
            elif left_expr.type == "literal" and right_expr.type == "variable":
                # strategy: load left into temp, and operate
                left_value = left_expr.data[0]
                right_reg = self.map_register(right_expr.data[0])
                asm_lines.append(f"  addi {self.temp_reg}, zero, {left_value}")
                asm_lines.append(f"  {target_insn} {dest_reg}, {self.temp_reg}, {right_reg}")
            elif left_expr.type == "variable" and right_expr.type == "literal":
                # strategy: load right into temp, and operate
                left_reg = self.map_register(left_expr.data[0])
                right_value = right_expr.data[0]
                asm_lines.append(f"  addi {self.temp_reg}, zero, {right_value}")
                asm_lines.append(f"  {target_insn} {dest_reg}, {left_reg}, {self.temp_reg}")
            elif left_expr.type == "variable" and right_expr.type == "variable":
                # strategy: directly operate
                left_reg = self.map_register(left_expr.data[0])
                right_reg = self.map_register(right_expr.data[0])
                asm_lines.append(f"  {target_insn} {dest_reg}, {left_reg}, {right_reg}")
        else:
            raise ValueError(f"Unsupported right expression type: {right.type}")

        return [f"  // {left} = {right}"] + asm_lines + [""]  # add a blank line for readability
    
    def compile(self) -> list:
        # load the library file
        with open(LIB_FILE, "r") as lib_file:
            lib_lines = lib_file.readlines()
        
        output = []
        
        # translate each parsed statement into assembly
        output.append("\n\n// BEGIN USER CODE")
        output.append(".text")

        # boilerplate
        output.append("main:")
        output.append("  // prologue")
        output.append("  addi sp, sp, -16")  # allocate stack space
        output.append("  sw 12(sp), ra")      # save return address

        for left, right in self.parser.code.lines:
            asm_lines = self.compile_statement(left, right)
            output.extend(asm_lines)

        output.append("  // epilogue")
        output.append("  jal ra, print_state")  # print variable state
        output.append("  lw ra, 12(sp)")      # restore return address
        output.append("  addi sp, sp, 16")    # deallocate stack space
        output.append("  jalr zero, ra")      # return
    
        return lib_lines + [line + "\n" for line in output]


if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 2:
        print("Please enter the name of the source file and output file")
        print(f"Usage: python3 {sys.argv[0]} <source_file> <output_file>")
        sys.exit(1)

    src_filename = sys.argv[1]

    asm_parser = parse_file(src_filename)

    for i, (left, right) in enumerate(asm_parser.code.lines):
        print(f"{i}: \t{left} = {right}")
    
    compiler = Compiler(asm_parser)
    asm_output = compiler.compile()

    output_filename = sys.argv[2]

    with open(output_filename, "w") as output_file:
        output_file.writelines(asm_output)
    print(f"Assembly output written to {output_filename}")


