from sly import Parser
from lab1.scanner_sly import Scanner
import os
import AST

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

    @_('instructions')  # type: ignore
    def instructions_opt(self, p):
        return p[0]

    @_('')  # type: ignore
    def instructions_opt(self, p):
        return p

    @_('instructions instruction')  # type: ignore
    def instructions(self, p):
        return p[0], p[1]

    @_('instruction')  # type: ignore
    def instructions(self, p):
        return p[0]

    @_('PRINT elements LINE_END')  # type: ignore
    def instruction(self, p):
        # print(p.elements)
        return AST.ArgumentInstruction(name=p[0], args=p[1])

    @_('RETURN expr LINE_END')  # type: ignore
    def instruction(self, p):
        return AST.ArgumentInstruction(name=p[0], args=p[1])

    @_('BREAK LINE_END',  # type: ignore
       'CONTINUE LINE_END')
    def instruction(self, p):
        return p[0]

    @_('LBRACE instructions RBRACE')  # type: ignore
    def instruction(self, p):
        return p[1]

    @_('IF LPAREN expr RPAREN instruction %prec IFX')  # type: ignore
    def instruction(self, p):
        return AST.ConditionalInstruction(condition=p[2], instructions=p[4], else_instruction=None)

    @_('IF LPAREN expr RPAREN instruction ELSE instruction')  # type: ignore
    def instruction(self, p):
        return AST.ConditionalInstruction(condition=p[2], instructions=p[4], else_instruction=p[6])

    @_('WHILE LPAREN expr RPAREN instruction')  # type: ignore
    def instruction(self, p):
        return AST.WhileLoop(condition=p[2], instructions=p[5])

    @_('FOR ID ASSIGN expr RANGE expr instruction')  # type: ignore
    def instruction(self, p):
        return AST.ForLoop(id=p[1], range_start=p[3], range_end=p[5], instructions=p[6])

    @_('assignment LINE_END')  # type: ignore
    def instruction(self, p):
        return p[0]

    @_('ID assign expr')  # type: ignore
    def assignment(self, p):
        return AST.Assignment(id=p[0], assign_type=p[1], value=p[2])

    @_('ID LBRACKET elements RBRACKET assign expr')  # type: ignore
    def assignment(self, p):
        return AST.AssignIndex(id=p[0], index=p[2], assign_type=p[4], value=p[5])

    @_('ASSIGN',  # type: ignore
       'ADDASSIGN',
       'SUBASSIGN',
       'MULASSIGN',
       'DIVASSIGN')
    def assign(self, p):
        return p[0]

    @_(# type: ignore
        # ARITHMETIC
       'expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr',
       # MATRIX
       'expr DOTADD expr',  # type: ignore
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr'
       )
    def expr(self, p):
        return AST.BinExpr(op=p[1], left=p[0], right=p[2])

    @_('expr EQ expr', # type: ignore
       'expr NEQ expr',
       'expr LTE expr',
       'expr GTE expr',
       'expr LT expr',
       'expr GT expr')
    def expr(self, p):
        return AST.RelationExpr(op=p[1], left=p[0], right=p[2])

    @_('LPAREN expr RPAREN')  # type: ignore
    def expr(self, p):
        return p[1]

    @_('INTNUM')  # type: ignore
    def expr(self, p):
        return p[0]

    @_('FLOATNUM')  # type: ignore
    def expr(self, p):
        return p[0]

    @_('STRING')  # type: ignore
    def expr(self, p):
        return p[0]

    @_('ID')  # type: ignore
    def expr(self, p):
        return p[0]

    @_('EYE LPAREN elements RPAREN',  # type: ignore
       'ZEROS LPAREN elements RPAREN',
       'ONES LPAREN elements RPAREN')
    def expr(self, p):
        return AST.MatrixFunction(name=p[0], params=p[2])

    @_('MINUS expr %prec UMINUS')  # type: ignore
    def expr(self, p):
        return AST.UnaryExpr(op=p[0], value=p[1])

    @_('vector')  # type: ignore
    def expr(self, p):
        return p[0]

    @_('LBRACKET elements RBRACKET')  # type: ignore
    def vector(self, p):
        return AST.Vector(p[1])

    @_('expr COMMA elements')  # type: ignore
    def elements(self, p):
        return p[0], p[2]

    @_('expr')  # type: ignore
    def elements(self, p):
        return p[0]

    @_('expr TRANSPOSE')  # type: ignore
    def expr(self, p):
        return AST.UnaryExpr(op=p[1], value=p[0])
