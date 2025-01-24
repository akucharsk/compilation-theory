class Token() :
    def __init__(self, text, symbol, representation) :
        self.text = text
        self.symbol = symbol
        self.representation = representation
        
    def check(self, symbol) :
        return self.text == symbol or self.symbol == symbol or self.representation == symbol
        
    def __repr__(self) :
        return self.representation
    
    def __add__(self, other, field = 'text', self_first = True) :
        if isinstance(other, str) :
            other = Token(other, None, other.capitalize())
        if not isinstance(other, Token) : 
            raise Exception(f"Unable to concatenate types of {type(self)} and {type(other)}")
        
        if not hasattr(self, field) or not hasattr(other, field):
            raise AttributeError(f"Field '{field}' does not exist in Token objects")
        
        output = [getattr(self, field), getattr(other, field)]
        
        return output[0] + output[1] if self_first else output[1] + output[0]
    
    def __radd__(self, other, field = 'text') :
        return self.__add__(other, field, self_first = False)
    
    
            

# PLUS = "PLUS"
# PLUS_OP = "+"
# MINUS = "MINUS"
# MINUS_OP = "-"
# TIMES = "TIMES"
# TIMES_OP = "*"
# DIVIDE = "DIVIDE"
# DIVIDE_OP = "/"
# ASSIGN = "ASSIGN"
# ASSIGN_OP = "="
# ADDASSIGN = "ADDASSIGN"
# ADDASSIGN_OP = "+="
# SUBASSIGN = "SUBASSIGN"
# SUBASSIGN_OP = "-=" 
# MULASSIGN = "MULASSIGN"
# MULASSIGN_OP = "*=" 
# DIVASSIGN = "DIVASSIGN"
# DIVASSIGN_OP = "/="

# LPAREN = "LPAREN"
# LPAREN_OP = "("
# RPAREN = "RPAREN"
# RPAREN_OP = ")"
# LBRACE = "LBRACE"
# LBRACE_OP = "{"
# RBRACE = "RBRACE"
# RBRACE_OP = "}"
# LBRACKET = "LBRACKET"
# LBRACKET_OP = "["
# RBRACKET = "RBRACKET"
# RBRACKET_OP = "]"

# DOTADD = "DOTADD"
# DOTADD_OP = ".+"
# DOTSUB = "DOTSUB"
# DOTSUB_OP = ".-"
# DOTMUL = "DOTMUL"
# DOTMUL_OP = ".*"
# DOTDIV = "DOTDIV"
# DOTDIV_OP = "./"

# EQ = "EQ"
# EQ_OP = "=="
# NEQ = "NEQ"
# NEQ_OP = "!="
# LT = "LT"
# LT_OP = "<"
# LTE = "LTE"
# LTE_OP = "<="
# GT = "GT"
# GT_OP = ">"
# GTE = "GTE"
# GTE_OP = ">="

# EQ = Token("EQ", "==", "Eq")
# NEQ = Token("NEQ", "!=", "Neq")
# LT = Token("LT", "<", "Lt")
# LTE = Token("LTE", "<=", "Lte")
# GT = Token("GT", ">", "Gt")
# GTE = Token("GTE", ">=", "Gte")

# RANGE = "RANGE"
# RANGE_PRINT = "Range"
# COLON = "COLON"
# COLON_OP = ":"
# COMMA = "COMMA"
# COMMA_OP = ","
# LINE_END = "LINE_END"
# LINE_END_OP = ";"
# TRANSPOSE = "TRANSPOSE"

# TRANSPOSE_OP = "'"
# FOR = "FOR"
# FOR_PRINT = "For"
# WHILE = "WHILE"
# WHILE_PRINT = "While"
# IF = "IF"
# IF_PRINT = "If"
# IFX = "IFX"
# IFX_PRINT = "Ifx"
# ELSE = "ELSE"
# ELSE_PRINT = "Else"
# IF_ELSE = "IF_ELSE"
# IF_ELSE_PRINT = "If-Else"
# THEN = "THEN"
# THEN_PRINT = "Then"
# RETURN = "RETURN"
# RETURN_PRINT = "Return"
# BREAK = "BREAK"
# BREAK_PRINT = "Break"
# CONTINUE = "CONTINUE"
# CONTINUE_PRINT = "Continue"
# EYE = "EYE"
# EYE_PRINT = "Eye"
# ZEROS = "ZEROS"
# ZEROS_PRINT = "Zeros"
# ONES = "ONES"
# ONES_PRINT = "Ones"
# PRINT = "PRINT"
# PRINT_PRINT = "Print"

# ID = "ID"
# INTNUM = "INTNUM"
# INTNUM_PRINT = "IntNum"
# FLOATNUM = "FLOATNUM"
# FLOATNUM_PRINT = "FloatNum"
# STRING = "STRING"
# STRING_PRINT = "String"

# ID = Token("ID", None, "Id")
# INTNUM = Token("INTNUM", None, "IntNum")
# FLOATNUM = Token("FLOATNUM", None, "FloatNum")
# STRING = Token("STRING", None, "String")

# MATRIX_ASSIGN = "MATRIX_ASSIGN"
# MATRIX_ASSIGN_PRINT = "MatrixAssign"
# MATRIX_READ = "MATRIX_READ"
# MATRIX_READ_PRINT = "MatrixRead"
# MATRIX = "MATRIX"
# MATRIX_PRINT = "Matrix"
# INDEX = "INDEX"
# INDEX_PRINT = "Index"

# VAR = "VAR"
# VAR_PRINT = "Var"
# UMINUS = "UMINUS"
# UMINUS_OP = "-"
# UMINUS_PRINT = "Unary Minus"
# UNKNOWN = "UNKNOWN"
# UNKNOWN_PRINT = "Unknown"
# BOOL = "BOOL"
# BOOL_PRINT = "Bool"

TOKENS = []

# Operators
PLUS = Token("PLUS", "+", "Plus")
TOKENS.append(PLUS)
MINUS = Token("MINUS", "-", "Minus")
TOKENS.append(MINUS)
TIMES = Token("TIMES", "*", "Times")
TOKENS.append(TIMES)
DIVIDE = Token("DIVIDE", "/", "Divide")
TOKENS.append(DIVIDE)
ASSIGN = Token("ASSIGN", "=", "Assign")
TOKENS.append(ASSIGN)
ADDASSIGN = Token("ADDASSIGN", "+=", "Addassign")
TOKENS.append(ADDASSIGN)
SUBASSIGN = Token("SUBASSIGN", "-=", "Subassign")
TOKENS.append(SUBASSIGN)
MULASSIGN = Token("MULASSIGN", "*=", "Mulassign")
TOKENS.append(MULASSIGN)
DIVASSIGN = Token("DIVASSIGN", "/=", "Divassign")
TOKENS.append(DIVASSIGN)

# Parentheses and brackets
LPAREN = Token("LPAREN", "(", "Lparen")
TOKENS.append(LPAREN)
RPAREN = Token("RPAREN", ")", "Rparen")
TOKENS.append(RPAREN)
LBRACE = Token("LBRACE", "{", "Lbrace")
TOKENS.append(LBRACE)
RBRACE = Token("RBRACE", "}", "Rbrace")
TOKENS.append(RBRACE)
LBRACKET = Token("LBRACKET", "[", "Lbracket")
TOKENS.append(LBRACKET)
RBRACKET = Token("RBRACKET", "]", "Rbracket")
TOKENS.append(RBRACKET)

# Dot operators
DOTADD = Token("DOTADD", ".+", "Dotadd")
TOKENS.append(DOTADD)
DOTSUB = Token("DOTSUB", ".-", "Dotsub")
TOKENS.append(DOTSUB)
DOTMUL = Token("DOTMUL", ".*", "Dotmul")
TOKENS.append(DOTMUL)
DOTDIV = Token("DOTDIV", "./", "Dotdiv")
TOKENS.append(DOTDIV)

# Relational operators
EQ = Token("EQ", "==", "Eq")
TOKENS.append(EQ)
NEQ = Token("NEQ", "!=", "Neq")
TOKENS.append(NEQ)
LT = Token("LT", "<", "Lt")
TOKENS.append(LT)
LTE = Token("LTE", "<=", "Lte")
TOKENS.append(LTE)
GT = Token("GT", ">", "Gt")
TOKENS.append(GT)
GTE = Token("GTE", ">=", "Gte")
TOKENS.append(GTE)

# Miscellaneous tokens
RANGE = Token("RANGE", ":", "Range")
TOKENS.append(RANGE)
COLON = Token("COLON", ":", "Colon")
TOKENS.append(COLON)
COMMA = Token("COMMA", ",", "Comma")
TOKENS.append(COMMA)
LINE_END = Token("LINE_END", ";", "LineEnd")
TOKENS.append(LINE_END)
TRANSPOSE = Token("TRANSPOSE", "'", "Transpose")
TOKENS.append(TRANSPOSE)

# Keywords
FOR = Token("FOR", None, "For")
TOKENS.append(FOR)
WHILE = Token("WHILE", None, "While")
TOKENS.append(WHILE)
IF = Token("IF", None, "If")
TOKENS.append(IF)
IFX = Token("IFX", None, "Ifx")
TOKENS.append(IFX)
ELSE = Token("ELSE", None, "Else")
TOKENS.append(ELSE)
IF_ELSE = Token("IF_ELSE", None, "If-Else")
TOKENS.append(IF_ELSE)
THEN = Token("THEN", None, "Then")
TOKENS.append(THEN)
RETURN = Token("RETURN", None, "Return")
TOKENS.append(RETURN)
BREAK = Token("BREAK", None, "Break")
TOKENS.append(BREAK)
CONTINUE = Token("CONTINUE", None, "Continue")
TOKENS.append(CONTINUE)
EYE = Token("EYE", None, "Eye")
TOKENS.append(EYE)
ZEROS = Token("ZEROS", None, "Zeros")
TOKENS.append(ZEROS)
ONES = Token("ONES", None, "Ones")
TOKENS.append(ONES)
PRINT = Token("PRINT", None, "Print")
TOKENS.append(PRINT)

# Data types and literals
ID = Token("ID", None, "Id")
TOKENS.append(ID)
INTNUM = Token("INTNUM", None, "Int")
TOKENS.append(INTNUM)
FLOATNUM = Token("FLOATNUM", None, "Float")
TOKENS.append(FLOATNUM)
STRING = Token("STRING", None, "String")
TOKENS.append(STRING)

# Matrix-related tokens
MATRIX_ASSIGN = Token("MATRIX_ASSIGN", None, "MatrixAssign")
TOKENS.append(MATRIX_ASSIGN)
MATRIX_ACCESS = Token("MATRIX_ACCESS", None, "MatrixAccess")
TOKENS.append(MATRIX_ACCESS)
MATRIX = Token("MATRIX", None, "Matrix")
TOKENS.append(MATRIX)
INDEX = Token("INDEX", None, "Index")
TOKENS.append(INDEX)

# Other tokens
VAR = Token("VAR", None, "Var")
TOKENS.append(VAR)
UMINUS = Token("UMINUS", "-", "UnaryMinus")
TOKENS.append(UMINUS)
UNKNOWN = Token("UNKNOWN", None, "Unknown")
TOKENS.append(UNKNOWN)
BOOL = Token("BOOL", None, "Bool")
TOKENS.append(BOOL)
NOT = Token("NOT", "!", "Not")
TOKENS.append(NOT)



def find_token(symbol) :
    if isinstance(symbol, Token) : return symbol
    if symbol is None : return UNKNOWN
    for token in TOKENS :
        if token.check(symbol) or token.check(symbol.upper()) : return token
    return UNKNOWN


COMPATIBLE = {}
COMPATIBLE[INTNUM] = {}
COMPATIBLE[INTNUM][INTNUM]  = [PLUS, MINUS, TIMES, DIVIDE]
COMPATIBLE[INTNUM][FLOATNUM]  = [PLUS, MINUS, TIMES, DIVIDE]
COMPATIBLE[INTNUM][STRING]  = [TIMES]
COMPATIBLE[INTNUM][MATRIX]  = [TIMES, DIVIDE, DOTADD, DOTSUB, DOTMUL, DOTDIV]

COMPATIBLE[FLOATNUM] = {}
COMPATIBLE[FLOATNUM][FLOATNUM]  = [PLUS, MINUS, TIMES, DIVIDE]
COMPATIBLE[FLOATNUM][STRING]  = []
COMPATIBLE[FLOATNUM][MATRIX]  = [TIMES, DIVIDE, DOTADD, DOTSUB, DOTMUL, DOTDIV]

COMPATIBLE[STRING] = {}
COMPATIBLE[STRING][STRING]  = [PLUS]
COMPATIBLE[STRING][MATRIX]  = []

COMPATIBLE[MATRIX] = {}
COMPATIBLE[MATRIX][MATRIX]  = [PLUS, MINUS, TIMES, DOTADD, DOTSUB, DOTMUL, DOTDIV]

def compatible(type1, type2, oper) :
    return oper in COMPATIBLE.get(type1, {}).get(type2, []) or oper in COMPATIBLE.get(type2, {}).get(type1, [])