# lol

MASK_32 = 0xFFFFFFFF
MASK_16 = 0xFFFF
MASK_8 = 0xFF
WORD_SIZE = 4  # 4 bytes for a 32-bit word
HALF_SIZE = 2  # 2 bytes for a 16-bit half
BYTE_SIZE = 1  # 1 byte

def trim_line(line):
    # there are strings, so we need to be careful about comments
    in_string = False
    escaped = False
    for i, char in enumerate(line):
        if char == '"' and not escaped:
            in_string = not in_string
        if char == '\\' and not escaped:
            escaped = True
        else:
            escaped = False
        if not in_string and char == '/' and i + 1 < len(line) and line[i + 1] == '/':
            return line[:i].strip()
    return line.strip()


class Parser:
    def __init__(self):
        self.code = []
        self.code_labels = []
        self.data = []  # bytes
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
                literal_num = int(word, 0) & MASK_32  # autodetects hex, binary too
                # store via little-endian
                self.data.append((literal_num >> 0) & MASK_8)
                self.data.append((literal_num >> 8) & MASK_8)
                self.data.append((literal_num >> 16) & MASK_8)
                self.data.append((literal_num >> 24) & MASK_8)

            return
        
        if kword == ".half":
            # add some halfword data
            if not self.mode == "data":
                raise ValueError("Can only declare data in a .data section")

            halves = [i.strip() for i in remaining_text.split(",")]
            halves = [i for i in halves if len(i) > 0]
            if not halves:
                raise ValueError("No data declared in .half section")

            for half in halves:
                literal_num = int(half, 0) & MASK_16  # autodetects hex, binary too
                # store via little-endian
                self.data.append((literal_num >> 0) & MASK_8)
                self.data.append((literal_num >> 8) & MASK_8)

            return
        
        if kword == ".byte":
            # add some byte data
            if not self.mode == "data":
                raise ValueError("Can only declare data in a .data section")

            bytes_list = [i.strip() for i in remaining_text.split(",")]
            bytes_list = [i for i in bytes_list if len(i) > 0]
            if not bytes_list:
                raise ValueError("No data declared in .byte section")

            for byte in bytes_list:
                literal_num = int(byte, 0) & MASK_8  # autodetects hex, binary too
                self.data.append(literal_num)

            return
        
        if kword == ".zero":
            # add some zeroed bytes
            if not self.mode == "data":
                raise ValueError("Can only declare data in a .data section")
            num_zeros = int(remaining_text.strip(), 0)
            for _ in range(num_zeros):
                self.data.append(0)
            return
        
        if kword == ".string":
            # add a string as byte data in C-string format
            if not self.mode == "data":
                raise ValueError("Can only declare data in a .data section")
            
            remaining_text = remaining_text.strip()

            if not (remaining_text.startswith('"') and remaining_text.endswith('"')):
                raise ValueError(".string data must be enclosed in double quotes")

            string_content = remaining_text[1:-1]  # remove quotes

            escaped = False
            processed_string = ""

            for char in string_content:
                if escaped:
                    if char == 'n':
                        processed_string += '\n'
                    elif char == 't':
                        processed_string += '\t'
                    elif char == '"':
                        processed_string += '"'
                    elif char == '\\':
                        processed_string += '\\'
                    else:
                        raise ValueError(f"Unknown escape sequence: \\{char}")
                    escaped = False
                else:
                    if char == '\\':
                        escaped = True
                    else:
                        processed_string += char

            for char in processed_string:
                self.data.append(ord(char) & MASK_8)
            self.data.append(0)  # null-terminate the string

            return
        
        if kword == ".align":
            # align the data/code to a word boundary
            if not self.mode == "data":  # only usable in data section for now
                raise ValueError("Can only align data in a .data section")
            align_to = int(remaining_text.strip(), 0)
            current_len = len(self.data)
            padding_needed = (align_to - (current_len % align_to)) % align_to
            for _ in range(padding_needed):
                self.data.append(0)
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

def print_asm(asm, comment=None, line_num=None, comment_col=32, line_num_col=4):
    asm_line = asm if comment is None else f"{asm.ljust(comment_col - 1)} // {comment}"
    header = " " * (line_num_col + 2) if line_num is None else f"{line_num:0{line_num_col}x}  " 
    print(header + asm_line)

def dump_asm(parser):
    print("Code:")
    print("============")
    for i in range(len(parser.code)):
        for label in parser.code_labels[i]:
            print_asm(f"{label}:", "jump target label")

        insn, args = parser.code[i]
        print_asm(f"    {insn:<8}{', '.join(args)}", line_num=i)

    print("\nData:")
    print("============")
    data_start_addr = 256
    for i in range(len(parser.data)):
        for label in parser.data_labels[i]:
            print_asm(f"{label}:", "data reference label")

        data_word = parser.data[i]
        print_asm(f"    {hex(data_word)}", line_num=data_start_addr + i)

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
