from sly import Parser
from scanner_sly import Scanner



class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'

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

    @_('instructions')
    def instructions_opt(self, p):
        pass

    @_('')
    def instructions_opt(self, p):
        pass

    @_('instructions instruction')
    def instructions(self, p):
        return p

    @_('instruction')
    def instructions(self, p):
        return p

    @_('PRINT elements LINE_END')
    def instruction(self, p):
        print(p.elements)
        return p

    @_('RETURN expr LINE_END')
    def instruction(self, p):
        return p

    @_('BREAK LINE_END',
       'CONTINUE LINE_END')
    def instruction(self, p):
        return p

    @_('LBRACE instructions RBRACE')
    def instruction(self, p):
        return p

    @_('IF LPAREN expr RPAREN instruction %prec IFX')
    def instruction(self, p):
        return p

    @_('IF LPAREN expr RPAREN instruction ELSE instruction')
    def instruction(self, p):
        return p

    @_('WHILE LPAREN expr RPAREN instruction')
    def instruction(self, p):
        return p

    @_('FOR ID ASSIGN expr RANGE expr instruction')
    def instruction(self, p):
        return p

    @_('assignment LINE_END')
    def instruction(self, p):
        return p

    @_('ID assign expr')
    def assignment(self, p):
        return p

    @_('ID LBRACKET elements RBRACKET assign expr')
    def assignment(self, p):
        return p

    @_('ASSIGN',
       'ADDASSIGN',
       'SUBASSIGN',
       'MULASSIGN',
       'DIVASSIGN')
    def assign(self, p):
        return p

    @_('expr EQ expr',
       'expr NEQ expr',
       'expr LT expr',
       'expr GT expr',
       'expr LTE expr',
       'expr GTE expr')
    def expr(self, p):
        return p

    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr')
    def expr(self, p):
        return p

    @_('expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return p

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p

    @_('INTNUM')
    def expr(self, p):
        return p

    @_('FLOATNUM')
    def expr(self, p):
        return p

    @_('STRING')
    def expr(self, p):
        return p

    @_('ID')
    def expr(self, p):
        return p

    @_('EYE LPAREN elements RPAREN',
       'ZEROS LPAREN elements RPAREN',
       'ONES LPAREN elements RPAREN')
    def expr(self, p):
        return p

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return p

    @_('vector')
    def expr(self, p):
        return p

    @_('LBRACKET elements RBRACKET')
    def vector(self, p):
        return p

    @_('expr COMMA elements')
    def elements(self, p):
        return p

    @_('expr')
    def elements(self, p):
        return p

    @_('expr TRANSPOSE')
    def expr(self, p):
        return p
