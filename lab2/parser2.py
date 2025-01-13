from sly import Parser
from lab1.scanner_sly import Scanner
from tokens_names import *
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
debug_path = os.path.join(SCRIPT_PATH, "parser_debug_data", "parser.out")

if not os.path.exists(debug_path):
    os.makedirs(os.path.dirname(debug_path), exist_ok=True)

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = debug_path

    precedence = (
        ('left', DOTADD, DOTSUB),       # Operatory elementarne
        ('left', PLUS, MINUS),         # Operatory macierzowe
        ('left', DOTMUL, DOTDIV),      # Operatory elementarne mnożenia/dzielenia
        ('left', TIMES, DIVIDE),       # Operatory macierzowe mnożenia/dzielenia
        ('right', UMINUS),             # Unary minus
        ('right', TRANSPOSE)           # Transpozycja
    )




    start = 'program'
    
    def __init__(self):
        super().__init__()
        
    # Program -> Instructions
    @_(f'instructions') # type: ignore
    def program(self, p):
        return p.instructions

    # Instructions -> Instruction Instructions
    @_(f'instruction instructions') # type: ignore
    def instructions(self, p):
        return [p.instruction] + p.instructions
    
    # Instructions -> Epsilon
    @_(f'epsilon') # type: ignore
    def instructions(self, p):
        return []
    
    # Instruction -> Assignment LINE_END
    @_(f'assignment {LINE_END}') # type: ignore
    def instruction(self, p):
        return p.assignment
        pass
    
    # Instruction -> Loop
    @_(f'loop') # type: ignore
    def instruction(self, p):
        return p.loop
        pass
    
    # Instruction -> IfElse
    @_(f'if_else') # type: ignore
    def instruction(self, p):
        return p.IfElse
        pass
    
    # Instruction -> Print LINE_END
    @_(f'print_ {LINE_END}') # type: ignore
    def instruction(self, p):
        return p.print_
        pass
    
    # Instruction -> Expression LINE_END
    @_(f'expression {LINE_END}') # type: ignore
    def instruction(self, p):
        return p.expression
        pass
    
    # Instruction -> Break LINE_END
    @_(f'break_ {LINE_END}') # type: ignore
    def instruction(self, p):
        return p.break_
        pass
    
    # Instuction -> Continue LINE_END
    @_(f'continue_ {LINE_END}') # type: ignore
    def instruction(self, p):
        return p.continue_
        pass
    
    # Instruction -> Return LINE_END
    @_(f'return_ {LINE_END}') # type: ignore
    def instruction(self, p):
        return p.return_
        pass
    
    # Epsilon -> ε
    @_(f'') # type: ignore
    def epsilon(self, p):
        return None
        pass
    
    # Assignment -> IdExpression AssignOp Expression
    @_(f'id_expression assign_op expression') # type: ignore
    def assignment(self, p):
        return ('assign', p.id_expression, p.assign_op, p.expression)
        pass
    
    # AssignOp -> ASSIGN
    # AssignOp -> ADDASSIGN
    # AssignOp -> SUBASSIGN
    # AssignOp -> MULASSIGN
    # AssignOp -> DIVASSIGN
    @_(ASSIGN, ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN) # type: ignore
    def assign_op(self, p):
        return p[0]
        pass
    
    # IDEpression -> ID Indexes
    @_(f'{ID} indexes') # type: ignore
    def id_expression(self, p):
        return ('id', p.ID, p.indexes)
        pass
    
    # Indexes -> LBRACKET Expression RBRACKET Indexes
    # Indexes -> LBRACKET Elements RBRACKET Indexes
    @_(f'{LBRACKET} expression {RBRACKET} indexes',  # type: ignore
       f'{LBRACKET} elements {RBRACKET} indexes')
    def indexes(self, p):
        # return Indexes(p.expression)
        return [p[1]] + p.indexes
        pass
    
    # @_(f'{LBRACKET} elements {RBRACKET} indexes') # type: ignore
    # def indexes(self, p):
    #     # return Indexes(p.expression)
    #     # return [p.elements] + p.indexes
    #     pass
    
    # Indexes -> Epsilon
    @_(f'epsilon') # type: ignore
    def indexes(self, p):
        return []
        pass
    
    # Loop -> FOR ID ASSIGN RANGE LBRACE Instructions RBRACE
    @_(f'{FOR} {ID} {ASSIGN} range {LBRACE} instructions {RBRACE}') # type: ignore
    def loop(self, p):
        return ('for', p.ID, p.range, p.instructions)
        pass
    
    # Loop -> WHILE LPAREN Boolean RPAREN LBRACE Instructions RBRACE
    @_(f'{WHILE} {LPAREN} boolean {RPAREN} {LBRACE} instructions {RBRACE}') # type: ignore
    def loop(self, p):
        return ('while', p.boolean, p.instructions)
        pass
    
    # IfElse -> matched_if_else
    @_(f'matched_if_else') # type: ignore
    def if_else(self, p):
        return p.matched_if_else
        pass
    
    # IfElse -> unmatched_if_else
    @_(f'unmatched_if_else') # type: ignore
    def if_else(self, p):
        return p.unmatched_if_else
        pass
    
    # MatchedIfElse -> IF LPAREN Boolean RPAREN LBRACE Instructions RBRACE ELSE LBRACE Instructions RBRACE
    @_(f'{IF} {LPAREN} boolean {RPAREN} {LBRACE} instructions {RBRACE} {ELSE} {LBRACE} instructions {RBRACE}') # type: ignore
    def matched_if_else(self, p):
        return ('if_else', p.boolean, p.instructions0, p.instructions1)
        pass
    
    # MatchedIfElse -> IF LPAREN Boolean RPAREN LBRACE Instructions RBRACE ElseIfList ELSE LBRACE Instructions RBRACE
    @_(f'{IF} {LPAREN} boolean {RPAREN} {LBRACE} instructions {RBRACE} else_if_list {ELSE} {LBRACE} instructions {RBRACE}') # type: ignore
    def matched_if_else(self, p):
        return ('if_else', p.boolean, p.instructions0, p.else_if_list, p.instructions1)
        pass
    
    
    
    # UnmatchedIfElse -> IF LPAREN Boolean RPAREN LBRACE Instructions RBRACE
    @_(f'{IF} {LPAREN} boolean {RPAREN} {LBRACE} instructions {RBRACE}') # type: ignore
    def unmatched_if_else(self, p):
        return ('if_else', p.boolean, p.instructions0)
        pass
    
    
    
    # UnmatchedIfElse -> IF LPAREN Boolean RPAREN LBRACE Instructions RBRACE ElseIfList
    @_(f'{IF} {LPAREN} boolean {RPAREN} {LBRACE} instructions {RBRACE} else_if_list') # type: ignore
    def unmatched_if_else(self, p):
        return ('if_else', p.boolean, p.instructions0, p.else_if_list)
        pass
    
    # UnmatchedIfElse -> IF LPAREN Boolean RPAREN LBRACE Instructions RBRACE ELSE UnmatchedIfElse
    @_(f'{IF} {LPAREN} boolean {RPAREN} {LBRACE} instructions {RBRACE} {ELSE} unmatched_if_else') # type: ignore
    def unmatched_if_else(self, p):
        return ('if_else', p.boolean, p.instructions0, p.unmatched_if_else)
        pass
    
    # ElseIfList -> ELSE IF LPAREN Boolean RPAREN LBRACE Instructions RBRACE
    @_(f'{ELSE} {IF} {LPAREN} boolean {RPAREN} {LBRACE} instructions {RBRACE}') # type: ignore
    def else_if_list(self, p):
        return ('else_if', p.boolean, p.instructions)
        pass
    
    # ElseIfList -> ELSE IF LPAREN Boolean RPAREN LBRACE Instructions RBRACE ElseIfList
    @_(f'{ELSE} {IF} {LPAREN} boolean {RPAREN} {LBRACE} instructions {RBRACE} else_if_list') # type: ignore
    def else_if_list(self, p):
        return ('else_if', p.boolean, p.instructions, p.else_if_list)
        pass
    
    # Print -> PRINT LPAREN Elements RPAREN
    @_(f'{PRINT} {LPAREN} elements {RPAREN}', # type: ignore
       f'{PRINT} elements')
    def print_(self, p):
        return ('print', p.elements)
        pass
    
    
    # Expression -> Term
    @_(f'term')
    def expression(self, p):
        return p.term
    

    # Expression -> Term BinOp Expression
    @_(f'term bin_op expression')
    def expression(self, p):
        return ('binary_op', p.bin_op, p.term, p.expression)
    

    # Term -> Factor
    @_(f'factor')
    def term(self, p):
        return p.factor
    

    # Term -> Factor HighOp Term
    @_(f'factor high_op term')
    def term(self, p):
        return ('high_op', p.high_op, p.factor, p.term)
    
    # Factor -> LPAREN Expression RPAREN
    @_(f'{LPAREN} expression {RPAREN}') # type: ignore
    def factor(self, p):
        return p.expression
        pass
    
    # Factor -> UMINUS Factor
    @_(f'{UMINUS} factor') # type: ignore
    def factor(self, p):
        return ('uminus', p.UMINUS, p.factor)
        pass
    
    # Factor -> IDExpression
    @_(f'id_expression') # type: ignore
    def factor(self, p):
        return p.id_expression
        pass
    
    # Factor -> Variable
    @_(f'variable') # type: ignore
    def factor(self, p):
        return p.variable
        pass
    
    # Factor -> Range
    @_(f'range') # type: ignore
    def factor(self, p):
        return p.range
        pass
    
    # Factor -> Factor TRANSPOSE
    @_(f'factor {TRANSPOSE}') # type: ignore
    def factor(self, p):
        return ('transpose', p.factor)
        pass
    
    # HighOp -> TIMES
    # HighOp -> DIVIDE
    # HighOp -> DOTMUL
    # HighOp -> DOTDIV
    @_(TIMES, DIVIDE, DOTMUL, DOTDIV) # type: ignore
    def high_op(self, p):
        return p[0]
        pass
    
    # BinOp -> PLUS
    # BinOp -> MINUS
    # BinOp -> DOTADD
    # BinOp -> DOTSUB
    @_(PLUS, MINUS, DOTADD, DOTSUB) # type: ignore
    def bin_op(self, p):
        return p[0]
        pass
    
    # Variable -> INTNUM
    # Variable -> FLOATNUM
    # Variable -> STRING
    # Variable -> Matrix
    # Variable -> Boolean
    @_(INTNUM, FLOATNUM, STRING, 'matrix', 'boolean') # type: ignore
    def variable(self, p):
        return p[0]
        pass
    
    # Matrix -> LBRACKET Elements RBRACKET
    @_(f'{LBRACKET} elements {RBRACKET}') # type: ignore
    def matrix(self, p):
        return ('matrix', p.elements)
        pass
    
    # Matrix -> MatrixFunction LPAREN Expression RPAREN
    @_(f'matrix_function {LPAREN} expression {RPAREN}') # type: ignore
    def matrix(self, p):
        return ('matrix_function', p.matrix_function, p.expression)
        pass
    
    # MatrixFunction -> ONES
    # MatrixFunction -> ZEROS
    # MatrixFunction -> EYE
    @_(ONES, ZEROS, EYE) # type: ignore
    def matrix_function(self, p):
        return p[0]
        pass
    
    
    # Range -> Expression COLON Expression
    @_(f'expression {COLON} expression') # type: ignore
    def range(self, p):
        return ('range', p.expression0, p.expression1)
        pass
    
    # CondOp -> LT
    # CondOp -> LTE
    # CondOp -> GT
    # CondOp -> GTE
    # CondOp -> EQ
    # CondOp -> NEQ
    @_(LT, LTE, GT, GTE, EQ, NEQ) # type: ignore
    def cond_op(self, p):
        return p[0]
        pass
    
    # Boolean -> BOOLEAN
    @_(BOOLEAN) # type: ignore
    def boolean(self, p):
        return p[0]
        pass
    
    # Boolean -> LPAREN Boolean RPAREN
    @_(f'{LPAREN} boolean {RPAREN}') # type: ignore
    def boolean(self, p):
        return p.boolean
        pass
    
    # Boolean -> Boolean LogicOp Boolean
    @_(f'boolean logic_op boolean') # type: ignore
    def boolean(self, p):
        return ('logic_op', p.boolean0, p.logic_op, p.boolean1)
        pass
    
    # Boolean -> Not Boolean
    @_(f'not_ boolean') # type: ignore
    def boolean(self, p):
        return ('not', p.not_, p.boolean)
        pass
    
    # Boolean -> Expression CondOp Expression
    @_(f'expression cond_op expression') # type: ignore
    def boolean(self, p):
        return ('cond_op', p.expression0, p.cond_op, p.expression1)
        pass
    
    # Not -> NOT
    # Not -> NOTC
    @_(NOT, NOTC) # type: ignore
    def not_(self, p):
        # return p[0]
        pass
    
    # LogicOp -> Or
    # LogicOp -> And
    @_('or_', 'and_') # type: ignore
    def logic_op(self, p):
        return p[0]
        pass
    
    # Or -> OR
    # Or -> ORC
    @_(OR, ORC) # type: ignore
    def or_(self, p):
        return p[0]
        pass
    
    # And -> AND
    # And -> ANDC
    @_(AND, ANDC) # type: ignore
    def and_(self, p):
        return p[0]
        pass
    
    # Elements -> Elements COMMA Expression
    @_(f'elements {COMMA} expression') # type: ignore
    def elements(self, p):
        return [p.elements] + p.expression
        pass
    
    # Elements -> Expression
    @_(f'expression') # type: ignore
    def elements(self, p):
        return p.expression
        pass
    
    # Break -> BREAK
    @_(BREAK) # type: ignore
    def break_(self, p):
        return BREAK
        pass
    
    # Continue -> CONTINUE
    @_(CONTINUE) # type: ignore
    def continue_(self, p):
        return CONTINUE
        pass
    
    # Return -> RETURN
    @_(RETURN) # type: ignore
    def return_(self, p):
        return RETURN
        pass
    
    # Return -> RETURN Elements
    @_(f'{RETURN} elements') # type: ignore
    def return_(self, p):
        return ('return', p.elements)
        pass
    