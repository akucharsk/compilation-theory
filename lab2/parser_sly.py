from sly import Parser
from lab1.scanner_sly import Scanner
import os
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
debug_path = os.path.join(SCRIPT_PATH, "parser_debug_data", "parser.out")

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = debug_path

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("nonassoc", 'EQ', 'NEQ'),
        ("nonassoc", 'LT', 'GT', 'LTE', 'GTE'),
        ("left", 'PLUS', 'MINUS', 'DOTADD', 'DOTSUB'),
        ("left", 'TIMES', 'DIVIDE', 'DOTMUL', 'DOTDIV'),
        ("right", 'UMINUS'),
        ("left", 'TRANSPOSE'),
    )

    def __init__(self):
        super().__init__()
        self.variables = {}

    @_('instructions') # type: ignore
    def instructions_opt(self, p):
        pass

    @_('') # type: ignore
    def instructions_opt(self, p):
        pass

    @_('instructions instruction') # type: ignore
    def instructions(self, p):
        return p

    @_('instruction') # type: ignore
    def instructions(self, p):
        return p

    @_('PRINT elements LINE_END') # type: ignore
    def instruction(self, p):
        # print(p.elements)
        return p

    @_('RETURN expr LINE_END') # type: ignore
    def instruction(self, p):
        return p

    @_('BREAK LINE_END', # type: ignore
       'CONTINUE LINE_END')
    def instruction(self, p):
        return p

    @_('LBRACE instructions RBRACE') # type: ignore
    def instruction(self, p):
        return p

    @_('IF LPAREN expr RPAREN instruction %prec IFX') # type: ignore
    def instruction(self, p):
        return p

    @_('IF LPAREN expr RPAREN instruction ELSE instruction') # type: ignore
    def instruction(self, p):
        return p

    @_('WHILE LPAREN expr RPAREN instruction') # type: ignore
    def instruction(self, p):
        return p

    @_('FOR ID ASSIGN expr RANGE expr instruction') # type: ignore
    def instruction(self, p):
        return p

    @_('assignment LINE_END') # type: ignore
    def instruction(self, p):
        return p

    @_('ID assign expr') # type: ignore
    def assignment(self, p):
        return p

    @_('ID LBRACKET elements RBRACKET assign expr') # type: ignore
    def assignment(self, p):
        return p

    @_('ASSIGN', # type: ignore
       'ADDASSIGN',
       'SUBASSIGN',
       'MULASSIGN',
       'DIVASSIGN')
    def assign(self, p):
        return p

    @_('expr EQ expr', # type: ignore
       'expr NEQ expr',
       'expr LT expr',
       'expr GT expr',
       'expr LTE expr',
       'expr GTE expr')
    def expr(self, p):
        return p

    @_('expr PLUS expr', # type: ignore
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr')
    def expr(self, p):
        return p

    @_('expr DOTADD expr', # type: ignore
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return p

    @_('LPAREN expr RPAREN') # type: ignore
    def expr(self, p):
        return p

    @_('INTNUM') # type: ignore
    def expr(self, p):
        return p

    @_('FLOATNUM') # type: ignore
    def expr(self, p):
        return p

    @_('STRING') # type: ignore
    def expr(self, p):
        return p

    @_('ID') # type: ignore
    def expr(self, p):
        return p

    @_('EYE LPAREN elements RPAREN', # type: ignore
       'ZEROS LPAREN elements RPAREN',
       'ONES LPAREN elements RPAREN')
    def expr(self, p):
        return p

    @_('MINUS expr %prec UMINUS') # type: ignore
    def expr(self, p):
        return p

    @_('vector') # type: ignore
    def expr(self, p):
        return p

    @_('LBRACKET elements RBRACKET') # type: ignore
    def vector(self, p):
        return p

    @_('expr COMMA elements') # type: ignore
    def elements(self, p):
        return p

    @_('expr') # type: ignore
    def elements(self, p):
        return p

    @_('expr TRANSPOSE') # type: ignore
    def expr(self, p):
        return p