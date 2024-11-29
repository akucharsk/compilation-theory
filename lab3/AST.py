from dataclasses import dataclass
from typing import Any, List

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

class Node(object):
    pass

# INSTRUCTIONS

@dataclass
class CompoundStatement(Node):
    instructions: List[Node]

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
    value: Any

@dataclass
class ContinueInstruction(Node):
     value: Any


# EXPRESSIONS

@dataclass
class IntNum(Node):
    value: int

@dataclass
class FloatNum(Node):
    value: float

@dataclass
class Variable(Node):
    name: str

@dataclass
class BinExpr(Node):
    op: str
    left: Node
    right: Node

@dataclass
class RelationExpr(Node):
    op: str
    left: Node
    right: Node

@dataclass
class UnaryExpr(Node):
    op: str
    value: Node

@dataclass
class Transpose(Node):
    value: Node

@dataclass
class String(Node):
    value: str


# ASSIGNMENTS

@dataclass
class Assignment(Node):
    id: Any
    assign_type: str
    value: Any

@dataclass
class AssignIndex(Node):
    id: Any
    index: Any
    assign_type: str
    value: Any


# LOOPS

@dataclass
class ForLoop(Node):
    id: Any
    range: Node
    instructions: Any

@dataclass
class WhileLoop(Node):
    condition: Any
    instructions: Any


# ARRAYS AND RANGES

@dataclass
class Vector(Node):
    elements: List[Any]

@dataclass
class ArrayAccess(Node):
    id: Node
    indices: List[Node]

@dataclass
class Range(Node):
    start: Any
    end: Any


# FUNCTIONS

@dataclass
class MatrixFunction(Node):
    name: str
    params: List[Node]


# ERROR

@dataclass
class Error(Node):
    message: str

