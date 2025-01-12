from sly import Parser
from lab1.scanner_sly import Scanner
from tokens_names import *

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'

    precedence = (
        (f'left', OR, ORC),
        (f'left', AND, ANDC),
        (f'right', NOT),
        (f'left', LT, LTE, GT, GTE, EQ, NEQ),
        (f'left', PLUS, MINUS, DOTADD, DOTSUB),
        (f'left', TIMES, DIVIDE, DOTMUL, DOTDIV),
        (f'right', UMINUS, TRANSPOSE),
    )

    @_(f'instructions') # type: ignore
    def program(self, p):
        return p.instructions

    @_(f'instruction instructions') # type: ignore
    def instructions(self, p):
        return [p.instruction] + p.instructions
    
    @_(f'epsilon') # type: ignore
    def instructions(self, p):
        return []
    
    @_(f'assignment {LINE_END}') # type: ignore
    def instruction(self, p):
        # return p.assignment
        pass
    
    @_(f'loop') # type: ignore
    def instruction(self, p):
        # return p.loop
        pass
    
    @_(f'if_else') # type: ignore
    def instruction(self, p):
        # return p.IfElse
        pass
    
    @_(f'print {LINE_END}') # type: ignore
    def instruction(self, p):
        # return p.print
        pass
    
    @_(f'expression {LINE_END}') # type: ignore
    def instruction(self, p):
        # return p.expression
        pass
    
    @_(f'break {LINE_END}') # type: ignore
    def instruction(self, p):
        # return p.break
        pass
    
    @_(f'continue {LINE_END}') # type: ignore
    def instruction(self, p):
        # return p.continue
        pass
    
    @_(f'return {LINE_END}') # type: ignore
    def instruction(self, p):
        # return p.return
        pass
    
    @_(f'') # type: ignore
    def epsilon(self, p):
        # return None
        pass
    
    @_(f'id_expression assign_op expression') # type: ignore
    def assignment(self, p):
        # return Assignment(p.id_expression, p.assign_op, p.expression)
        pass
    
    @_(ASSIGN, ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN) # type: ignore
    def assign_op(self, p):
        # return p[0]
        pass
    
    @_(f'{ID} indexes') # type: ignore
    def id_expression(self, p):
        # return IdExpression(p.ID, p.indexes)
        pass
    
    @_(f'{LBRACKET} expression {RBRACKET} indexes')  # type: ignore
    def indexes(self, p):
        # return Indexes(p.expression)
        # return [p.expression] + p.indexes
        pass
    
    @_(f'{LBRACKET} elements {RBRACKET} indexes') # type: ignore
    def indexes(self, p):
        # return Indexes(p.expression)
        # return [p.elements] + p.indexes
        pass
    
    @_('epsilon') # type: ignore
    def indexes(self, p):
        # return []
        pass
    
    