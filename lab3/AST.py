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


# EXPRESSIONS


@dataclass
class BinExpr(Node):
    op: Any
    left: Any
    right: Any


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
      
