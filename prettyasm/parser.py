import re
from typing import List
from lexer import LexedFile, SectionFileLexer


class Parser:
    def __init__(self):
        # curr variables are temporary variables used during parsing of a single procedure
        self.curr_code = []  # List[Tuple[str, List[str]]], contains tuple of insn, args tokens in each line of code
        self.curr_code_labels = []  # List[List[str]], parallel to code, each entry is a list of labels for that instruction

        self.output_code_lines = []  # List[str]
        self.output_data_lines = []  # List[str]

    def _init_curr_procedure(self):
        self.curr_code = []
        self.curr_code_labels = []
    
    def _pad_label_list(self):
        # fills the label list with empty values
        self.curr_code_labels.extend([] for i in range(len(self.curr_code) - len(self.curr_code_labels)))
    
    def _add_curr_code_label(self, label_name):
        label_idx = len(self.curr_code)
        self.curr_code_labels.extend([] for i in range(label_idx - len(self.curr_code_labels) + 1))
        self.curr_code_labels[label_idx].append(label_name)
    
    def _parse_prettyasm_line(self, line):
        kword, *remaining = line.split(" ", 1)
        remaining_text = remaining[0] if remaining else ""

        if kword.endswith(":"):
            self._add_curr_code_label(kword[:-1])
            return

        if kword in (".word", ".half", ".byte", ".zero", ".string", ".align"):
            raise ValueError("Data directives are not allowed in a .prettyasm section")

        args = [i.strip() for i in remaining_text.split(",")]
        args = [i for i in args if len(i) > 0]
        self.curr_code.append((kword, args))
        self._pad_label_list()  # ensure label list is same length as code list
    
    def _substitute_labels(self) -> List[str]:  # generates lines of code from curr
        output_label_lines = [[] for _ in self.curr_code_labels]  # List[List[str]]
        output_code = [[] for _ in self.curr_code]  # List[Tuple[str, List[str]]]

        # first, collect a list of all @label references
        # and map them to (line_idx, label_num)
        curr_label_num = 0
        label_references = {}  # maps label name to (line_idx, label_num)
        for code_line, labels in enumerate(self.curr_code_labels):
            for label in labels:
                if not label.startswith("@"):
                    # global label, just copy it to the output
                    # just can't be a numerical label like 0, 1, etc
                    if re.match(r'^\d+$', label):
                        raise ValueError(f"Invalid global label name: {label}")
                    output_label_lines[code_line].append(label)  # add label to output code
                    continue
                if label in label_references:
                    raise ValueError(f"Duplicate label reference: {label}")
                label_references[label] = (code_line, curr_label_num)
                output_label_lines[code_line].append(f"{curr_label_num}:  // local label {label}")  # add numerical label to output code
                curr_label_num += 1

        # next, substitute all @label references in the code with their line numbers
        for line_idx, (insn, args) in enumerate(self.curr_code):
            def substitute_arg(arg: str) -> str:
                if arg.startswith("@"):
                    if arg not in label_references:
                        raise ValueError(f"Undefined label reference: {arg}")
                    target_line, label_num = label_references[arg]
                    if target_line <= line_idx:
                        return f'{label_num}b'  # backward reference
                    else:
                        return f'{label_num}f'  # forward reference
                return arg  # not a label reference, just return it as is
            substituted_args = tuple(substitute_arg(arg) for arg in args)
            output_code[line_idx] = (insn, substituted_args)

        # now, combine the output labels and code into final output lines
        output_lines = []
        for label_lines, (insn, args) in zip(output_label_lines, output_code):
            for label in label_lines:
                output_lines.append(f"{label}")  # don't need to add any colons; already their own lines of code
            if insn:
                output_lines.append(f"  {insn} {', '.join(args)}")
        return output_lines
    
    def parse_prettyasm_section(self, lines: List[str]) -> List[str]:
        output_lines = []
        line_reader = iter(lines)
        for line in line_reader:
            # parse for procedure print_stuff:
            if line.startswith("procedure "):
                self._init_curr_procedure()
                procedure_name = line[len("procedure "):].strip()
                if not procedure_name.endswith(":"):
                    raise ValueError(f"Procedure declaration must end with a colon: {line}")
                procedure_name = procedure_name[:-1].strip()  # remove trailing colon
                output_lines.append(f"{procedure_name}:  // procedure start")
                for line in line_reader:
                    if line.strip() == "endprocedure;":
                        break
                    self._parse_prettyasm_line(line)
                else:
                    raise ValueError(f"Procedure {procedure_name} not properly terminated with endprocedure")
                
                output_lines.extend(self._substitute_labels())
                output_lines.append(f"// end procedure {procedure_name}")
                output_lines.append("")  # add blank line after each procedure
            else:
                raise ValueError(f"Unknown line format in .prettyasm section: {line}")
        return output_lines

    def compile_lexed_file(self, lexed_file: LexedFile) -> List[str]:
        # translates prettyasm file into normal assembly file
        output_code = []
        for section_name, section_lines in lexed_file.sections.items():
            if section_name == ".prettyasm":
                compiled_asm_code = self.parse_prettyasm_section(section_lines)
                output_code.append("section .text // compiled from .prettyasm")
                output_code.append("")
                output_code.extend(compiled_asm_code)
                output_code.append("// end of compiled .prettyasm text section")
            else:
                # directly copy other sections without modification
                output_code.append(f"section {section_name} // copied from original file")
                output_code.append("")
                output_code.extend(section_lines)
                output_code.append(f"// end of copied {section_name} section")
            output_code.append("")  # new line lol
        return output_code


def lex_file(filename):
    file_lexer = SectionFileLexer()
    return file_lexer.lex_file(filename)

def compile_lexed_file(lexed_file: LexedFile) -> List[str]:
    parser = Parser()
    return parser.compile_lexed_file(lexed_file)


if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 2:
        print("Please enter the name of the source file and output file")
        print(f"Usage: python3 {sys.argv[0]} <source_file> <output_file>")
        sys.exit(1)

    src_filename = sys.argv[1]

    lexed_file = lex_file(src_filename)
    compiled_code = compile_lexed_file(lexed_file)

    output_filename = sys.argv[2]


    with open(output_filename, "w") as f:
        f.write(f"// Compiled from {src_filename} using prettyasm parser\n\n")
        f.write("\n".join(compiled_code))
    print(f"Compiled assembly output written to {output_filename}")

    # test_procedure_lines = [
    #     "addi a0, zero, 67",
    #     "addi a1, zero, 94",
    #     "@loop:",
    #     "printc a0",
    #     "addi a0, a0, 1",
    #     "blt a0, a1, @loop",
    #     "jalr zero, ra"
    # ]

    # parser = Parser()
    # parser._init_curr_procedure()
    # for line in test_procedure_lines:
    #     parser._parse_prettyasm_line(line)
    
    # for i, line in enumerate(parser.curr_code):
    #     print(f"{i:02d}: {line}  labels: {parser.curr_code_labels[i]}")
    
    # output_lines = parser._substitute_labels()
    # print("Output lines:")
    # print("\n".join(output_lines))
