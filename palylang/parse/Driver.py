import sys
from antlr4 import *
from PalyLangLexer import PalyLangLexer
import sys
import itertools
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from PalyLangLexer import PalyLangLexer
from PalyLangParser import PalyLangParser


def escape_label(s: str) -> str:
    s = s.replace('\\', '\\\\')
    s = s.replace('\n', '\\n')
    s = s.replace('"', '\\"')
    return s


def node_label(node, parser):
    # Terminal nodes: show token name and text
    if isinstance(node, TerminalNodeImpl):
        text = node.getText()
        sym = node.getSymbol()
        if sym is not None:
            t = sym.type
            name = None
            if t >= 0 and t < len(parser.symbolicNames):
                name = parser.symbolicNames[t]
            if not name or name == '<INVALID>':
                # fallback to literal name
                if t >= 0 and t < len(parser.literalNames):
                    name = parser.literalNames[t]
            if name:
                return f"{escape_label(name)}\\n{escape_label(text)}"
        return escape_label(text)
    # Parser rule nodes: show rule name
    try:
        ri = node.getRuleIndex()
        if ri is not None and ri >= 0:
            return escape_label(parser.ruleNames[ri])
    except Exception:
        pass
    return escape_label(str(type(node)))


def tree_to_dot(tree, parser):
    lines = []
    lines.append('digraph ParseTree {')
    lines.append('  node [shape=box, fontsize=10, fontname="Courier"];')
    id_iter = itertools.count()

    def walk(node, parent_id=None):
        my_id = next(id_iter)
        label = node_label(node, parser)
        lines.append(f'  n{my_id} [label="{label}"];')
        if parent_id is not None:
            lines.append(f'  n{parent_id} -> n{my_id};')
        for i in range(node.getChildCount()):
            child = node.getChild(i)
            walk(child, my_id)

    walk(tree, None)
    lines.append('}')
    return '\n'.join(lines)


def main(argv):
    if len(argv) < 2:
        print('Usage: Driver.py <input-file> [--tree] [--dot out.dot]')
        return

    input_file = argv[1]
    opts = argv[2:]

    input_stream = FileStream(input_file)
    lexer = PalyLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PalyLangParser(stream)
    tree = parser.compilationUnit()

    # Default: do nothing visible. Offer options to print tree or emit dot.
    if '--tree' in opts:
        # LISP-style tree
        print(tree.toStringTree(recog=parser))

    if '--dot' in opts:
        # get filename after --dot
        try:
            idx = opts.index('--dot')
            out = opts[idx + 1]
        except Exception:
            out = 'parse_tree.dot'
        dot = tree_to_dot(tree, parser)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(dot)
        print(f'Wrote DOT to {out}')


if __name__ == '__main__':
    main(sys.argv)