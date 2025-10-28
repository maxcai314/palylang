# lol

def trim_line(line):
    # for now, since there are non strings, we can just trim after //
    without_comment = line.split("//", 1)[0]
    return without_comment.strip()


class Parser:
    def __init__(self):
        self.code = []
        self.code_labels = []
        self.data = []
        self.data_labels = []
        self.mode = None  # should be either "code" or "data"

    def parse_line(self, line):
        if line == ".text":
            self.mode = "code"
            return
        elif line == ".data":
            self.mode = "data"
            return

        kword, *remaining = line.split(" ", 1)
        remaining_text = remaining[0] if remaining else ""

        if kword.endswith(":"):
            # this line is a label
            label_name = kword[:-1]
            label_list = self.data_labels if self.mode == "data" else self.code_labels
            label_idx = len(self.data if self.mode == "data" else self.code)
            label_list.extend([] for i in range(label_idx - len(label_list) + 1))  # extend to fit
            label_list[label_idx].append(label_name)  # add the label to this line
            return

        if kword == ".word":
            # add some data
            if not self.mode == "data":
                raise ValueError("Can only declare data in a .data section")

            words = [i.strip() for i in remaining_text.split(",")]
            words = [i for i in words if len(i) > 0]
            if not words:
                raise ValueError("No data declared in .word section")

            for word in words:
                literal_num = int(word, 0)  # autodetects hex, binary too
                self.data.append(literal_num)

            return

        # otherwise, must be an asm insn
        if not self.mode == "code":
            raise ValueError("Can only declare insns in a .text section")

        args = [i.strip() for i in remaining_text.split(",")]
        args = [i for i in args if len(i) > 0]
        self.code.append((kword, args))

    def pad_label_list(self):
        # fills the label list with empty values
        for mode in ("data", "code"):
            label_list = self.data_labels if mode == "data" else self.code_labels
            label_idx = len(self.data if mode == "data" else self.code)
            label_list.extend([] for i in range(label_idx - len(label_list)))


def parse_lines(lines):
    parser = Parser()
    for line in lines:
        parser.parse_line(line)
    parser.pad_label_list()
    return parser

def print_asm(asm, comment=None, comment_col=32):
    asm_line = asm if comment is None else f"{asm.ljust(comment_col - 1)} // {comment}"
    print(asm_line)

def dump_asm(parser):
    print("Code:")
    print("============")
    for i in range(len(parser.code)):
        for label in parser.code_labels[i]:
            print_asm(f"{label}:", "jump target label")

        insn, args = parser.code[i]
        print_asm(f"    {insn:<8}{', '.join(args)}")

    print("\nData:")
    print("============")
    for i in range(len(parser.data)):
        for label in parser.data_labels[i]:
            print_asm(f"{label}:", "data reference label")

        data_word = parser.data[i]
        print_asm(f"    {hex(data_word)}")

def parse_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    # remove comments and whitespaces
    lines = [trim_line(line) for line in lines]
    lines = [line for line in lines if len(line) > 0]

    return parse_lines(lines)

if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        print("Please enter the name of the file to parse")
        sys.exit(1)

    filename = sys.argv[1]

    asm_parser = parse_file(filename)
    dump_asm(asm_parser)

    # you parse lines either in code or data mode, as you iterate.
    # in code mode, you append to a list of Tuple(insn, label)
    # in data mode, you append to a list of Tuple(word, label)
    # after accepting all, you do a pass through to resolve labels
    # local labels (integer, f/b) will traverse in direction until found
    # global labels will search entire file
    # global labels should be unique even between code/data
