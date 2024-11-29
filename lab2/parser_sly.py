from sly import Parser
from lab1.scanner_sly import Scanner
from lab3 import AST
import os
from tokens_names import *
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
debug_path = os.path.join(SCRIPT_PATH, "parser_debug_data", "parser.out")

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = debug_path

    precedence = (
        ("nonassoc", IFX),
        ("nonassoc", ELSE),
        ("nonassoc", EQ, NEQ),
        ("nonassoc", LT, GT, LTE, GTE),
        ("left", PLUS, MINUS, DOTADD, DOTSUB),
        ("left", TIMES, DIVIDE, DOTMUL, DOTDIV),
        ("right", UMINUS),
        ("left", TRANSPOSE),
    )

    def __init__(self):
        super().__init__()
        self.variables = {}

    @_('instructions') # type: ignore
    def instructions_opt(self, p):
        return AST.CompoundStatement(instructions=p.instructions)

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
        return AST.PrintInstruction(value=p.elements)

    @_('RETURN expr LINE_END') # type: ignore
    def instruction(self, p):
        return AST.ReturnInstruction(value=p.expr)

    @_('BREAK LINE_END', # type: ignore
    'CONTINUE LINE_END')
    def instruction(self, p):
        if p[0] == 'BREAK':
            return AST.BreakInstruction()
        elif p[0] == 'CONTINUE':
            return AST.ContinueInstruction()

    @_('LBRACE instructions RBRACE') # type: ignore
    def instruction(self, p):
        return p.instructions
    
    @_('IF LPAREN expr RPAREN instruction %prec IFX') # type: ignore
    def instruction(self, p):
        return AST.ConditionalInstruction(condition=p.expr, instructions=p.instruction, else_instruction=None)

    @_('IF LPAREN expr RPAREN instruction ELSE instruction') # type: ignore
    def instruction(self, p):
        return AST.ConditionalInstruction(condition=p.expr, instructions=p.instruction0, else_instruction=p.instruction1)

    @_('WHILE LPAREN expr RPAREN instruction') # type: ignore
    def instruction(self, p):
        return AST.WhileLoop(condition=p.expr, instructions=p.instruction)

    @_('FOR ID ASSIGN expr RANGE expr instruction') # type: ignore
    def instruction(self, p):
        return AST.ForLoop(id=p.ID, range=AST.Range(start=p.expr0, end=p.expr1), instructions=p.instruction)

    @_('assignment LINE_END') # type: ignore
    def instruction(self, p):
        return p.assignment

    @_('ID assign expr') # type: ignore
    def assignment(self, p):
        return AST.Assignment(id=p.ID, assign_type=p.assign, value=p.expr)

    @_('ID LBRACKET elements RBRACKET assign expr') # type: ignore
    def assignment(self, p):
        return AST.AssignIndex(id=p.ID, index=p.elements, assign_type=p.assign, value=p.expr)

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
        return AST.RelationExpr(op=p[1], left=p.expr0, right=p.expr1)

    @_('expr PLUS expr', # type: ignore
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr')
    def expr(self, p):
        return AST.BinExpr(op=p[1], left=p.expr0, right=p.expr1)

    @_('expr DOTADD expr', # type: ignore
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return AST.BinExpr(op=p[1], left=p.expr0, right=p.expr1)

    @_('LPAREN expr RPAREN') # type: ignore
    def expr(self, p):
        return p.expr

    @_('INTNUM') # type: ignore
    def expr(self, p):
        return AST.IntNum(value=p.INTNUM)

    @_('FLOATNUM') # type: ignore
    def expr(self, p):
        return AST.FloatNum(value=p.FLOATNUM)

    @_('STRING') # type: ignore
    def expr(self, p):
        return AST.String(value=p.STRING)

    @_('ID') # type: ignore
    def expr(self, p):
        return AST.Variable(name=p.ID)

    @_('EYE LPAREN elements RPAREN', # type: ignore
       'ZEROS LPAREN elements RPAREN',
       'ONES LPAREN elements RPAREN')
    def expr(self, p):
        return AST.MatrixFunction(name=p[0], params=p.elements)

    @_('MINUS expr %prec UMINUS') # type: ignore
    def expr(self, p):
        return AST.UnaryExpr(op='-', value=p.expr)

    @_('vector') # type: ignore
    def expr(self, p):
        return p.vector

    @_('LBRACKET elements RBRACKET') # type: ignore
    def vector(self, p):
        return AST.Vector(elements=p.elements)

    @_('expr COMMA elements') # type: ignore
    def elements(self, p):
        return [p.expr] + p.elements

    @_('expr') # type: ignore
    def elements(self, p):
        return [p.expr]

    @_('expr TRANSPOSE') # type: ignore
    def expr(self, p):
        return AST.Transpose(value=p.expr)