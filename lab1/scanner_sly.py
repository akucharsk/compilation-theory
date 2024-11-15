import sys
from sly import Lexer
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


class Scanner(Lexer):

    ignore = r' \t'
    ignore_comment = r'#.*'
    ignore_newline = r'\n'

    tokens = {
        "PLUS", "MINUS", "TIMES", "DIVIDE", "ASSIGN", "ADDASSIGN",
        "SUBASSIGN", "MULASSIGN", "DIVASSIGN", "LPAREN", "RPAREN", "LBRACE", "RBRACE",
        "LBRACKET", "RBRACKET", "DOTADD", "DOTSUB", "DOTMUL", "DOTDIV",
        "EQ", "NEQ", "LT", "LTE", "GT", "GTE", "RANGE", "COMMA", "LINE_END", "TRANSPOSE",
        "FOR", "WHILE", "IF", "ELSE", "RETURN", "BREAK", "CONTINUE", "EYE", "ZEROS", "ONES", "PRINT",
        "ID", "INTNUM", "FLOATNUM", "STRING"
    }

    EQ = r'=='
    NEQ = r'!='
    LTE = r'<='
    LT = r'<'
    GTE = r'>='
    GT = r'>'

    ASSIGN = r'='
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'\/='

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'

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

    RANGE = r':'
    COMMA = r','
    LINE_END = r';'

    TRANSPOSE = r'\''

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ID['for'] = "FOR"
    ID['while'] = "WHILE"
    ID['if'] = "IF"
    ID['else'] = "ELSE"
    ID['return'] = "RETURN"
    ID['break'] = "BREAK"
    ID['continue'] = "CONTINUE"
    ID['eye'] = "EYE"
    ID['zeros'] = "ZEROS"
    ID['ones'] = "ONES"
    ID['print'] = "PRINT"
    _intnum = r'[+-]?\d+'
    _exp = r'[eE][+-]?\d+'
    _dot_num = rf'[+-]?\d*\.\d+({_exp})?'
    _num_dot = rf'[+-]?\d+\.({_exp})?'
    _int_exp = rf'{_intnum}{_exp}'
    FLOATNUM = rf'{_dot_num}|{_num_dot}|{_int_exp}'
    INTNUM = rf'{_intnum}'
    STRING = r'"([^"\\\n]|\\")*"'

    @_(r'\n') # type: ignore
    def ignore_newline(self, t):
        self.lineno += 1

    @_(FLOATNUM) # type: ignore
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'[+-]?\d*') # type: ignore
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*') # type: ignore
    def ignore_comment(self, t):
        pass


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example_full.txt"
        file = open(os.path.join(SCRIPT_PATH,filename), "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    print(text)
    lexer = Scanner()
    line = 1
    print(float('62.51E2'))
    for tok in lexer.tokenize(text):
        print(tok)
