from lab3 import AST
from tokens_names import *

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

def indent_string(indent = 0) :
    return "|  " * indent

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print(indent_string(indent) + str(self.value))

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(indent_string(indent) + self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print(indent_string(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print(indent_string(indent) + "=")
        print(indent_string(indent + 1) + self.id)
        self.value.printTree(indent + 1)

    @addToClass(AST.CompoundStatement)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)
            
    @addToClass(AST.String)
    def printTree(self, indent=0):
        print(indent_string(indent) + f'"{self.value}"')
        
    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        print(indent_string(indent) + self.name)
        for param in self.params:
            param.printTree(indent + 1)
            
    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print(indent_string(indent) + VECTOR)
        for element in self.elements:
            element.printTree(indent + 1)

    @addToClass(AST.AssignIndex)
    def printTree(self, indent=0):
        print(indent_string(indent) + "=")
        print(indent_string(indent + 1) + INDEX)
        print(indent_string(indent + 2) + self.id)
        for idx in self.index:
            idx.printTree(indent + 2)
        self.value.printTree(indent + 1)
        
    
    @addToClass(AST.ArrayAccess)
    def printTree(self, indent = 0) :
        print(indent_string(indent) + ARRAY_READ)
        print(indent_string(indent + 1) + self.id)
        for idx in self.indices :
            idx.printTree(indent + 2)
        
    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        print(indent_string(indent) + TRANSPOSE)
        self.value.printTree(indent + 1)


    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print(indent_string(indent) + FOR)
        print(indent_string(indent + 1) + self.id)
        self.range.printTree(indent + 1)
        for instruction in self.instructions:
            instruction.printTree(indent + 1)


    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print(indent_string(indent) + RANGE)
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)
        
    @addToClass(AST.PrintInstruction)
    def printTree(self, indent=0):
        print(indent_string(indent) + PRINT)
        if isinstance(self.value, list):
            for val in self.value:
                val.printTree(indent + 1)
        else:
            self.value.printTree(indent + 1)
            
            
    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print(indent_string(indent) + WHILE)
        self.condition.printTree(indent + 1)
        for instruction in self.instructions:
            instruction.printTree(indent + 1)



    @addToClass(AST.RelationExpr)
    def printTree(self, indent=0):
        print(indent_string(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)


    @addToClass(AST.ConditionalInstruction)
    def printTree(self, indent=0):
        print(indent_string(indent) + IF)
        self.condition.printTree(indent + 1)
        print(indent_string(indent) + THEN)
        self.instructions.printTree(indent + 1)
        if self.else_instruction:
            print(indent_string(indent) + ELSE)
            self.else_instruction.printTree(indent + 1)

    @addToClass(AST.ContinueInstruction)
    def printTree(self, indent = 0) :
        print(indent_string(indent) + CONTINUE)
    
    @addToClass(AST.BreakInstruction)
    def printTree(self, indent = 0) :
        print(indent_string(indent) + BREAK)
        
    @addToClass(AST.ReturnInstruction)
    def printTree(self, indent = 0) :
        print(indent_string(indent) + RETURN)
