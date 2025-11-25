
# pip install antlr4-python3-runtime

# Generate parser and tell ANTLR to look for token vocabulary in the output directory
# Run this script in the root directory of the project
cd palylang/parse
antlr4 -Dlanguage=Python3 PalyLangLexer.g4 PalyLangParser.g4 -o .