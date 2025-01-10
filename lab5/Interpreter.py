import numpy as np

import lab3.AST as AST
from lab4.SymbolTable import SymbolTable
from lab5.Memory import *
from lab5.Exceptions import  *
from lab5.visit import *
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):

    operator_functions = {
        "+": lambda x, y: x + y,
        ".+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        ".-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        ".*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
        "./": lambda x, y: x / y,
    }

    relation_operations = {
        "==": lambda x, y: x == y,
        "!=": lambda x, y: x != y,
        ">": lambda x, y: x > y,
        "<": lambda x, y: x < y,
        ">=": lambda x, y: x >= y,
        "<=": lambda x, y: x <= y,
    }

    assignment_functions = {
        "+=": lambda x, y: x + y,
        "-=": lambda x, y: x - y,
        "*=": lambda x, y: x * y,
        "/=": lambda x, y: x / y,
    }

    matrix_functions = {
        "ones": lambda params: np.ones(tuple(params)),
        "zeros": lambda params: np.zeros(tuple(params)),
        "eye": lambda params: np.eye(*params)
    }

    unary_expressions = {
        "-": lambda x: -x,
        "!": lambda x: not x
    }

    def __init__(self):
        self.globalMemory = MemoryStack(Memory("global"))

    @on('node')
    def visit(self, node):
        print("[visit(node)] THIS LAB IS DOGSHIT")
        pass

    @when(AST.CompoundStatement)
    def visit(self, node: AST.CompoundStatement):
        for instruction in node.instructions:
            self.visit(instruction)

    @when(AST.BreakInstruction)
    def visit(self, node: AST.BreakInstruction):
        raise BreakException()

    @when(AST.ContinueInstruction)
    def visit(self, node: AST.ContinueInstruction):
        raise ContinueException()

    @when(AST.Variable)
    def visit(self, node: AST.Variable):
        return self.globalMemory.get(node.name)

    @when(AST.String)
    def visit(self, node: AST.String):
        return node.value.strip('"')

    @when(AST.FloatNum)
    def visit(self, node: AST.FloatNum):
        return node.value

    @when(AST.IntNum)
    def visit(self, node: AST.IntNum):
        return node.value

    @when(AST.Vector)
    def visit(self, node: AST.Vector):
        return np.array([elem] for elem in node.elements)

    @when(AST.ArrayAccess)
    def visit(self, node: AST.ArrayAccess):
        indices = node.indices if isinstance(node.indices, list) else [node.indices]
        index = [self.visit(idx) for idx in indices]
        return self.globalMemory.get(node.id)[*index]

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        return self.operator_functions[node.op](r1, r2)

    @when(AST.UnaryExpr)
    def visit(self, node: AST.UnaryExpr):
        r = self.visit(node.value)
        return self.unary_expressions[node.op](r)

    @when(AST.Transpose)
    def visit(self, node: AST.Transpose):
        return self.visit(node.value).T

    @when(AST.RelationExpr)
    def visit(self, node: AST.RelationExpr):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        return self.relation_operations[node.op](r1, r2)

    @when(AST.Assignment)
    def visit(self, node: AST.Assignment):
        node_value = self.visit(node.value)
        if node.assign_type == "=":
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
        print(*[self.visit(expr) for expr in node.value], sep=" ")

    @when(AST.MatrixFunction)
    def visit(self, node: AST.MatrixFunction):
        params = [self.visit(param) for param in node.params]
        key = node.name
        return self.matrix_functions[key](params)
