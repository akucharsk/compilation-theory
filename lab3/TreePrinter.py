from lab3 import AST
from tokens_names import *

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("|  " * indent + self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print("|  " * indent + "=")
        print("|  " * (indent + 1) + self.id)
        self.value.printTree(indent + 1)

    @addToClass(AST.CompoundStatement)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)
            
    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("|  " * indent + f'"{self.value}"')
        
    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        print("|  " * indent + self.name)
        for param in self.params:
            param.printTree(indent + 1)
            
    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print("|  " * indent + VECTOR)
        for element in self.elements:
            element.printTree(indent + 1)

    @addToClass(AST.AssignIndex)
    def printTree(self, indent=0):
        print("|  " * indent + "=")
        print("|  " * (indent + 1) + INDEX)
        print("|  " * (indent + 2) + self.id)
        for idx in self.index:
            idx.printTree(indent + 2)
        self.value.printTree(indent + 1)
        
        
    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        print("|  " * indent + TRANSPOSE)
        self.value.printTree(indent + 1)


    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print("|  " * indent + FOR)
        print("|  " * (indent + 1) + self.id)
        self.range.printTree(indent + 1)
        for instruction in self.instructions:
            instruction.printTree(indent + 1)


    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("|  " * indent + RANGE)
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)
        
    @addToClass(AST.PrintInstruction)
    def printTree(self, indent=0):
        print("|  " * indent + PRINT)
        if isinstance(self.value, list):
            for val in self.value:
                val.printTree(indent + 1)
        else:
            self.value.printTree(indent + 1)
            
            
    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print("|  " * indent + WHILE)
        self.condition.printTree(indent + 1)
        for instruction in self.instructions:
            instruction.printTree(indent + 1)



    @addToClass(AST.RelationExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)


    @addToClass(AST.ConditionalInstruction)
    def printTree(self, indent=0):
        print("|  " * indent + IF)
        self.condition.printTree(indent + 1)
        print("|  " * indent + THEN)
        if isinstance(self.instructions, list):
            for instruction in self.instructions:
                instruction.printTree(indent + 1)
        else:
            self.instructions.printTree(indent + 1)
        if self.else_instruction:
            print("|  " * indent + ELSE)
            if isinstance(self.else_instruction, list):
                for instruction in self.else_instruction:
                    instruction.printTree(indent + 1)
            else:
                self.else_instruction.printTree(indent + 1)










