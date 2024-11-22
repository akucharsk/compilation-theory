from dataclasses import dataclass
from typing import Any


class Node(object):
    pass


@dataclass
class IntNum(Node):
    value: Any


@dataclass
class FloatNum(Node):
    value: Any


@dataclass
class String(Node):
    value: Any


@dataclass
class Variable(Node):
    name: Any


@dataclass
class BinExpr(Node):
    op: Any
    left: Any
    right: Any


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


@dataclass
class MatrixFunction(Node):
    name: Any
    params: Any


@dataclass
class ForLoop(Node):
    range_start: Any
    range_end: Any
    instructions: Any


class Error(Node):
    def __init__(self):
        pass
      
