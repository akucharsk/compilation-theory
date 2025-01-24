from dataclasses import dataclass
from typing import Any, List

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

@dataclass
class Node:
    @property
    def children(self):
        return []


# INSTRUCTIONS


@dataclass
class CompoundStatement(Node):
    instructions: List[Node] = None
    line: int = None

@dataclass
class ConditionalInstruction(Node):
    condition: Any
    instructions: Any
    else_instruction: Any = None
    line: int = None

@dataclass
class PrintInstruction(Node):
    value: Any
    line: int = None


@dataclass
class ReturnInstruction(Node):
    value: Any
    line: int = None


@dataclass
class BreakInstruction(Node):
    value: Any = None
    line: int = None


@dataclass
class ContinueInstruction(Node):
    value: Any = None
    line: int = None


# EXPRESSIONS

@dataclass
class IntNum(Node):
    value: int
    line: int = None


@dataclass
class FloatNum(Node):
    value: float
    line: int = None


@dataclass
class Variable(Node):
    name: str
    line: int = None


@dataclass
class BinExpr(Node):
    op: str
    left: Node
    right: Node
    line: int = None


@dataclass
class RelationExpr(Node):
    op: str
    left: Node
    right: Node
    line: int = None


@dataclass
class UnaryExpr(Node):
    op: str
    value: Node
    line: int = None


@dataclass
class Transpose(Node):
    value: Node
    line: int = None


@dataclass
class String(Node):
    value: str
    line: int = None



# ASSIGNMENTS

@dataclass
class Assignment(Node):
    id: Any
    assign_type: str
    value: Any
    line: int = None


@dataclass
class AssignIndex(Node):
    id: Any
    index: Any
    assign_type: str
    value: Any
    line: int = None


# LOOPS

@dataclass
class Range(Node):
    start: Any
    end: Any
    line: int = None


@dataclass
class ForLoop(Node):
    id: Any
    range: Range
    instructions: Any
    line: int = None


@dataclass
class WhileLoop(Node):
    condition: Any
    instructions: Any
    line: int = None


# MATRICES AND RANGES

@dataclass
class Matrix(Node):
    elements: List[Any]
    line: int = None


@dataclass
class MatrixAccess(Node):
    id: Node
    indices: List[Node]
    line: int = None



# FUNCTIONS

@dataclass
class MatrixFunction(Node):
    name: str
    params: List[Node]
    line: int = None


# ERROR

@dataclass
class Error(Node):
    message: str
    line: int = None
