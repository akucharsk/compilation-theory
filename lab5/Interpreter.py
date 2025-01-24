import numpy as np

import lab3.AST as AST
from lab4.SymbolTable import SymbolTable
from lab5.Memory import *
from lab5.Exceptions import  *
from lab5.visit import *
from tokens_names import *
from util import matrix_divide

import sys

sys.setrecursionlimit(10000)


DEBUG = False


class Interpreter(object):

    operator_functions = {
        PLUS : lambda x, y: x + y,
        DOTADD : lambda x, y: x + y,
        MINUS : lambda x, y: x - y,
        DOTSUB : lambda x, y: x - y,
        TIMES : lambda x, y: x * y,
        DOTMUL : lambda x, y: x * y,
        DIVIDE : lambda x, y: x / y,
        DOTDIV : lambda x, y: x / y,
    }

    relation_operations = {
        EQ : lambda x, y: x == y,
        NEQ : lambda x, y: x != y,
        GT : lambda x, y: x > y,
        LT : lambda x, y: x < y,
        GTE : lambda x, y: x >= y,
        LTE : lambda x, y: x <= y,
    }

    assignment_functions = {
        ASSIGN : lambda x, y: y,
        ADDASSIGN : lambda x, y: x + y,
        SUBASSIGN : lambda x, y: x - y,
        MULASSIGN : lambda x, y: x * y,
        DIVASSIGN : lambda x, y: x / y,
    }

    matrix_functions = {
        ONES : lambda params: np.ones(tuple(params)),
        ZEROS : lambda params: np.zeros(tuple(params)),
        EYE : lambda params: np.eye(*params)
    }

    unary_expressions = {
        UMINUS : lambda x: -x,
        NOT: lambda x: not x
    }

    def __init__(self):
        self.globalMemory = MemoryStack(Memory("global"))

    @on('node')
    def visit(self, node):
        print("[visit(node)]")
        pass

    @when(AST.CompoundStatement)
    def visit(self, node: AST.CompoundStatement):
        if DEBUG: print("Visiting", node)
        for instruction in node.instructions:
            self.visit(instruction)

    @when(AST.BreakInstruction)
    def visit(self, node: AST.BreakInstruction):
        if DEBUG: print("Visiting", node)
        raise BreakException()

    @when(AST.ContinueInstruction)
    def visit(self, node: AST.ContinueInstruction):
        if DEBUG: print("Visiting", node)
        raise ContinueException()

    @when(AST.Variable)
    def visit(self, node: AST.Variable):
        if DEBUG: print("Visiting", node)
        return self.globalMemory.get(node.name)

    @when(AST.String)
    def visit(self, node: AST.String):
        if DEBUG: print("Visiting", node)
        return node.value.strip('"')

    @when(AST.FloatNum)
    def visit(self, node: AST.FloatNum):
        if DEBUG: print("Visiting", node)
        return node.value

    @when(AST.IntNum)
    def visit(self, node: AST.IntNum):
        if DEBUG: print("Visiting", node)
        return node.value

    @when(AST.Matrix)
    def visit(self, node: AST.Matrix):
        if DEBUG: print("Visiting", node)
        elements = []
        for element in node.elements :
            if isinstance(element, AST.Matrix) :
                subelements = []
                for subelement in element.elements :
                    subelements.append(subelement.value)
                elements.append(subelements)
            else :
                elements.append(element.value)
        return np.array(elements)

    @when(AST.MatrixAccess)
    def visit(self, node: AST.MatrixAccess):
        if DEBUG: print("Visiting", node)
        indices = node.indices if isinstance(node.indices, list) else [node.indices]
        index = [self.visit(idx) for idx in indices]
        return self.globalMemory.get(node.id)[*index]

    @when(AST.BinExpr)
    def visit(self, node):
        if DEBUG: print("Visiting", node)
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        if node.op == TIMES :
            return np.dot(r1, r2)
        if node.op == DIVIDE :
            return matrix_divide(r1, r2)
        return self.operator_functions[node.op](r1, r2)

    @when(AST.UnaryExpr)
    def visit(self, node: AST.UnaryExpr):
        if DEBUG: print("Visiting", node)
        r = self.visit(node.value)
        return self.unary_expressions[node.op](r)

    @when(AST.Transpose)
    def visit(self, node: AST.Transpose):
        if DEBUG: print("Visiting", node)
        return self.visit(node.value).T

    @when(AST.RelationExpr)
    def visit(self, node: AST.RelationExpr):
        if DEBUG: print("Visiting", node)
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        return self.relation_operations[node.op](r1, r2)

    @when(AST.Assignment)
    def visit(self, node: AST.Assignment):
        if DEBUG: print("Visiting", node)
        node_value = self.visit(node.value)
        if node.assign_type == ASSIGN :
            try:
                self.globalMemory.get(node.id)
                self.globalMemory.set(node.id, node_value)
            except NoSuchVariableException:
                self.globalMemory.insert(node.id, node_value)
        else:
            current_value = self.globalMemory.get(node.id)
            new_value = self.assignment_functions[node.assign_type](current_value, node_value)
            self.globalMemory.set(node.id, new_value)

    @when(AST.AssignIndex)
    def visit(self, node: AST.AssignIndex):
        if DEBUG: print("Visiting", node)
        node_value = self.visit(node.value)
        index = node.index if isinstance(node.index, list) else [node.index]
        index = [self.visit(idx) for idx in index]
        tensor = self.globalMemory.get(node.id)
        if node.assign_type == "=":
            tensor[*index] = node_value
        else:
            tensor[*index] = self.assignment_functions[node.assign_type](tensor[*index], node_value)

    @when(AST.ConditionalInstruction)
    def visit(self, node: AST.ConditionalInstruction):
        if DEBUG: print("Visiting", node)
        cond = self.visit(node.condition)
        r = None

        self.globalMemory.push(Memory("if"))
        if cond:
            for instruction in node.instructions:
                r = self.visit(instruction)
        self.globalMemory.pop()
        if node.else_instruction is not None:
            self.globalMemory.push(Memory("else"))
            for instruction in node.else_instruction:
                r = self.visit(instruction)
            self.globalMemory.pop()

        return r

    # simplistic while loop interpretation
    @when(AST.WhileLoop)
    def visit(self, node: AST.WhileLoop):
        if DEBUG: print("Visiting", node)
        r = None
        self.globalMemory.push(Memory("while"))
        instructions = node.instructions if isinstance(node.instructions, list) else [node.instructions]
        try:
            while self.visit(node.condition):
                try:
                    for instruction in instructions:
                        r = self.visit(instruction)
                except ContinueException:
                    pass
        except BreakException:
            pass
        self.globalMemory.pop()
        return r

    @when(AST.ForLoop)
    def visit(self, node: AST.ForLoop):
        if DEBUG: print("Visiting", node)
        range_start = self.visit(node.range.start)
        range_end = self.visit(node.range.end)
        self.globalMemory.push(Memory("for"))
        self.globalMemory.insert(node.id, range_start)

        r = None
        instructions = node.instructions if isinstance(node.instructions, list) else [node.instructions]
        try:
            for i in range(range_start, range_end):
                self.globalMemory.set(node.id, i)
                try:
                    for instruction in instructions:
                        r = self.visit(instruction)
                except ContinueException:
                    pass
        except BreakException:
            pass
        self.globalMemory.pop()
        return r

    @when(AST.PrintInstruction)
    def visit(self, node: AST.PrintInstruction):
        if DEBUG: print("Visiting", node)
        print(*[self.visit(expr) for expr in node.value], sep=" ")

    @when(AST.MatrixFunction)
    def visit(self, node: AST.MatrixFunction):
        if DEBUG: print("Visiting", node)
        params = [self.visit(param) for param in node.params]
        key = node.name
        return self.matrix_functions[key](params)
