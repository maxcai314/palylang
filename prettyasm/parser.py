# todo

from lexer import LexedFile, SectionFileLexer

def lex_file(filename):
    file_lexer = SectionFileLexer()
    return file_lexer.lex_file(filename)


if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        print("Please enter the name of the file to parse")
        sys.exit(1)

    filename = sys.argv[1]
    lexed_file = lex_file(filename)
    for section_name, lines in lexed_file.sections.items():
        print(f"Section: {section_name}")
        for line in lines:
            print(f"====  {line}")
