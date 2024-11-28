from sly import Parser
from lab1.scanner_sly import Scanner
import os
from tokens_names import *
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
        return p.instructions

    @_('') # type: ignore
    def instructions_opt(self, p):
        return []

    @_('instructions instruction') # type: ignore
    def instructions(self, p):
        return p.instructions + [p.instruction]

    @_('instruction') # type: ignore
    def instructions(self, p):
        return [p.instruction]

    @_('PRINT elements LINE_END') # type: ignore
    def instruction(self, p):
        return (PRINT, p.elements)

    @_('RETURN expr LINE_END') # type: ignore
    def instruction(self, p):
        return (RETURN, p.expr)

    @_('BREAK LINE_END', # type: ignore
    'CONTINUE LINE_END')
    def instruction(self, p):
        return p[0]

    @_('LBRACE instructions RBRACE') # type: ignore
    def instruction(self, p):
        return p.instructions
    
    @_('IF LPAREN expr RPAREN instruction %prec IFX') # type: ignore
    def instruction(self, p):
        return (IF, p.expr, p.instruction)

    @_('IF LPAREN expr RPAREN instruction ELSE instruction') # type: ignore
    def instruction(self, p):
        return (IF_ELSE, p.expr, p.instruction0, p.instruction1)

    @_('WHILE LPAREN expr RPAREN instruction') # type: ignore
    def instruction(self, p):
        return (WHILE, p.expr, p.instruction)

    @_('FOR ID ASSIGN expr RANGE expr instruction') # type: ignore
    def instruction(self, p):
        return (FOR, p.ID, p.expr0, p.expr1, p.instruction)

    @_('assignment LINE_END') # type: ignore
    def instruction(self, p):
        return p.assignment

    @_('ID assign expr') # type: ignore
    def assignment(self, p):
        return (ASSIGN, p.ID, p.assign, p.expr)

    @_('ID LBRACKET elements RBRACKET assign expr') # type: ignore
    def assignment(self, p):
        return (ARRAY_ASSIGN, p.ID, p.elements, p.assign, p.expr)

    @_('ASSIGN', # type: ignore
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN')
    def assign(self, p):
        return p[0]

    @_('expr EQ expr', # type: ignore
       'expr NEQ expr',
       'expr LT expr',
       'expr GT expr',
       'expr LTE expr',
       'expr GTE expr')
    def expr(self, p):
        return (p[1], p.expr0, p.expr1)

    @_('expr PLUS expr', # type: ignore
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr')
    def expr(self, p):
        return (p[1], p.expr0, p.expr1)

    @_('expr DOTADD expr', # type: ignore
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return (p[1], p.expr0, p.expr1)

    @_('LPAREN expr RPAREN') # type: ignore
    def expr(self, p):
        return p.expr

    @_('INTNUM') # type: ignore
    def expr(self, p):
        return (INTNUM, p.INTNUM)

    @_('FLOATNUM') # type: ignore
    def expr(self, p):
        return (FLOATNUM, p.FLOATNUM)

    @_('STRING') # type: ignore
    def expr(self, p):
        return (STRING, p.STRING) 

    @_('ID') # type: ignore
    def expr(self, p):
        return (VAR, p.ID)

    @_('EYE LPAREN elements RPAREN', # type: ignore
       'ZEROS LPAREN elements RPAREN',
       'ONES LPAREN elements RPAREN')
    def expr(self, p):
        return (p[0], p.elements)

    @_('MINUS expr %prec UMINUS') # type: ignore
    def expr(self, p):
        return (UMINUS, p.expr)

    @_('vector') # type: ignore
    def expr(self, p):
        return p.vector

    @_('LBRACKET elements RBRACKET') # type: ignore
    def vector(self, p):
        return (VECTOR, p.elements)

    @_('expr COMMA elements') # type: ignore
    def elements(self, p):
        return [p.expr] + p.elements

    @_('expr') # type: ignore
    def elements(self, p):
        return [p.expr]

    @_('expr TRANSPOSE') # type: ignore
    def expr(self, p):
        return (TRANSPOSE, p.expr)