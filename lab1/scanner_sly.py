import sys
from sly import Lexer


class Scanner(Lexer):

    ignore = r' \t'
    ignore_comment = r'#.*\n'
    ignore_newline = r'\n+'

    ADD = r'\+'
    SUB = r'-'
    MUL = r'\*'
    DIV = r'/'

    ASSIGN = r'='
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'\/='

    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LBRACKET = r'\['
    RBRACKET = r'\]'

    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'

    EQ = r'=='
    NEQ = r'!='
    LT = r'<'
    LTE = r'<='
    GT = r'>'
    GTE = r'>='

    RANGE = r':'
    COMMA = r','
    LINE_END = r';'

    TRANSPOSE = r'\''

    IF = r'if'
    ELSE = r'else'
    WHILE = r'while'
    FOR = r'for'

    BREAK = r'break'
    CONTINUE = r'continue'
    RETURN = r'return'

    EYE = r'eye'
    ZEROS = r'zeros'
    ONES = r'ones'

    PRINT = r'print'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    FLOATNUM = r'\d+\.|\d*\.\d+'
    INTNUM = r'[1-9]\d*'
    STRING = r'".*"'

    tokens = {"ADD", "SUB", "MUL", "DIV", "ASSIGN",
              "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN",
              "LPAREN", "RPAREN", "LBRACE", "RBRACE",
              "LBRACKET", "RBRACKET", "DOTADD",
              "DOTSUB", "DOTMUL", "DOTDIV",
              "EQ", "NEQ", "LT", "LTE", "GT", "GTE",
              "RANGE", "COMMA", "LINE_END", "TRANSPOSE",
              "IF", "ELSE", "WHILE", "FOR", "BREAK", "CONTINUE",
              "RETURN", "EYE", "ZEROS", "ONES", "PRINT", "ID",
              "INTNUM", "FLOATNUM", "STRING"}


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example_full.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    print(text)
    lexer = Scanner()
    line = 0
    for tok in lexer.tokenize(text):
        print(f'({line}): {tok.type}({tok.value})')
        # print(tok)
        if tok.type == 'LINE_END':
            line += 1
