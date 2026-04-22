# lol

from lexer import LexedSections, SectionFileLexer

MASK_32 = 0xFFFFFFFF
MASK_16 = 0xFFFF
MASK_8 = 0xFF
WORD_SIZE = 4  # 4 bytes for a 32-bit word
HALF_SIZE = 2  # 2 bytes for a 16-bit half
BYTE_SIZE = 1  # 1 byte


class Parser:
    def __init__(self):
        self.code = []
        self.code_labels = []
        self.data = []  # bytes
        self.data_labels = []

    def _add_code_label(self, label_name):
        label_idx = len(self.code)
        self.code_labels.extend([] for i in range(label_idx - len(self.code_labels) + 1))
        self.code_labels[label_idx].append(label_name)

    def _add_data_label(self, label_name):
        label_idx = len(self.data)
        self.data_labels.extend([] for i in range(label_idx - len(self.data_labels) + 1))
        self.data_labels[label_idx].append(label_name)

    def parse_code_line(self, line):
        kword, *remaining = line.split(" ", 1)
        remaining_text = remaining[0] if remaining else ""

        if kword.endswith(":"):
            self._add_code_label(kword[:-1])
            return

        if kword in (".word", ".half", ".byte", ".zero", ".string", ".align"):
            raise ValueError("Data directives are not allowed in a .text section")

        args = [i.strip() for i in remaining_text.split(",")]
        args = [i for i in args if len(i) > 0]
        self.code.append((kword, args))

    def parse_data_line(self, line):
        kword, *remaining = line.split(" ", 1)
        remaining_text = remaining[0] if remaining else ""

        if kword.endswith(":"):
            self._add_data_label(kword[:-1])
            return

        if kword == ".word":
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
            bytes_list = [i.strip() for i in remaining_text.split(",")]
            bytes_list = [i for i in bytes_list if len(i) > 0]
            if not bytes_list:
                raise ValueError("No data declared in .byte section")

            for byte in bytes_list:
                literal_num = int(byte, 0) & MASK_8  # autodetects hex, binary too
                self.data.append(literal_num)

            return

        if kword == ".zero":
            num_zeros = int(remaining_text.strip(), 0)
            for _ in range(num_zeros):
                self.data.append(0)
            return

        if kword == ".string":
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
            # align the data to a boundary in bytes
            align_to = int(remaining_text.strip(), 0)
            current_len = len(self.data)
            padding_needed = (align_to - (current_len % align_to)) % align_to
            for _ in range(padding_needed):
                self.data.append(0)
            return

        raise ValueError(f"Unknown data directive in .data section: {kword}")

    def parse_lexed_sections(self, lexed_sections: LexedSections):
        parsed_known_section = False

        for section_name in lexed_sections.section_order:
            section_lines = lexed_sections.get_section(section_name)

            if section_name == ".text":
                parsed_known_section = True
                for line in section_lines:
                    self.parse_code_line(line)
            elif section_name == ".data":
                parsed_known_section = True
                for line in section_lines:
                    self.parse_data_line(line)
            else:
                print(f"Warning: Ignoring unknown section {section_name}")

        if not parsed_known_section:
            raise ValueError("ASM file must contain at least one known section (.text or .data)")

        self.pad_label_list()

    def pad_label_list(self):
        # fills the label list with empty values
        self.data_labels.extend([] for i in range(len(self.data) - len(self.data_labels)))
        self.code_labels.extend([] for i in range(len(self.code) - len(self.code_labels)))


def parse_lines(lines):
    file_lexer = SectionFileLexer()
    lexed_file = file_lexer.lex_lines(lines)
    return parse_lexed_sections(lexed_file)


def parse_lexed_sections(lexed_sections: LexedSections):
    parser = Parser()
    parser.parse_lexed_sections(lexed_sections)
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
    file_lexer = SectionFileLexer()
    lexed_file = file_lexer.lex_file(filename)
    return parse_lexed_sections(lexed_file)

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
