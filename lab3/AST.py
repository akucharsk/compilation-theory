from dataclasses import dataclass
from typing import Any


class Node(object):
    pass


# INSTRUCTIONS


@dataclass
class ArgumentInstruction(Node):
    name: Any
    args: Any


@dataclass
class ConditionalInstruction(Node):
    condition: Any
    instructions: Any
    else_instruction: Any

@dataclass
class PrintInstruction(Node):
    value: Any


@dataclass
class ReturnInstruction(Node):
    value: Any


@dataclass
class BreakInstruction(Node):
    pass


@dataclass
class ContinueInstruction(Node):
    pass

# EXPRESSIONS

class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):

    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


@dataclass
class RelationExpr(Node):
    op: Any
    left: Node
    right: Node


@dataclass
class UnaryExpr(Node):
    op: Any
    value: Any


# ASSIGNMENTS


@dataclass
class Assignment(Node):
    id: Any
    assign_type: Any
    value: Any


@dataclass
class AssignIndex(Node):
    id: Any
    index: Any
    assign_type: Any
    value: Any


# LOOPS


@dataclass
class ForLoop(Node):
    id: Any
    range_start: Any
    range_end: Any
    instructions: Any


@dataclass
class WhileLoop(Node):
    condition: Any
    instructions: Any


# OTHER


@dataclass
class MatrixFunction(Node):
    name: Any
    params: Any


class Error(Node):
    def __init__(self):
        pass
      
