import random

from lab3 import AST
from lab4.SymbolTable import SymbolTable, VariableSymbol


class NodeVisitor(object):

    def __init__(self):
        self.errors = []

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)  # type: ignore

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            children = node.instructions
            for child in children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.in_loop = 0

        self.for_count = 0
        self.while_count = 0
        self.if_count = 0
        self.else_count = 0

        self.symbol_table = SymbolTable()

    def report_error(self, message):
        print(f"ERROR IN {message}")
        self.errors.append(message)

    def visit(self, node):
        if node is None:
            print("Visited: None")
            return
        if not isinstance(node, list):
            print(f"Visiting node: {type(node).__name__}, line: {getattr(node, 'line', 'unknown')}")

        try:
            return super().visit(node)
        except Exception as e:
            line = getattr(node, 'line', 'unknown')
            self.report_error(f"LINE {line}: {str(e)}")

    def visit_CompoundStatement(self, node):
        if not node.instructions:
            self.report_error(f"LINE {node.line}: Empty compound statement.")
            return
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_ConditionalInstruction(self, node):
        self.visit(node.condition)
        self.if_count += 1
        scope = self.symbol_table.pushScope(f'if_{self.if_count}')
        self.symbol_table.put(scope.name, scope)
        self.symbol_table = scope
        if node.instructions:
            self.visit(node.instructions)
        else:
            self.report_error(f"LINE {node.line}: Missing instructions in 'if' block.")

        self.symbol_table = scope.getParentScope()
        if node.else_instruction:
            self.else_count += 1
            scope = self.symbol_table.pushScope(f'else_{self.else_count}')
            self.symbol_table.put(scope.name, scope)
            self.symbol_table = scope
            self.visit(node.else_instruction)
            self.symbol_table = scope.getParentScope()

    def visit_PrintInstruction(self, node):
        if node.value is None:
            self.report_error(f"LINE {node.line}: Missing value in 'print' instruction.")
        else:
            self.visit(node.value)

    def visit_ReturnInstruction(self, node):
        if node.value is not None:
            self.visit(node.value)
        else:
            self.report_error(f"LINE {node.line}: 'return' statement with no value.")

    def visit_BreakInstruction(self, node):
        if self.in_loop == 0:
            self.report_error(f"LINE {node.line}: 'break' statement used outside of a loop.")

    def visit_ContinueInstruction(self, node):
        if self.in_loop == 0:
            self.report_error(f"LINE {node.line}: 'continue' statement used outside of a loop.")

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_Variable(self, node):

        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.report_error(f"Line {node.line}: Variable '{node.name}' is not defined.")
            return None
        return symbol.type

    def get_vector_size(self, node):
        if isinstance(node, AST.Variable):
            symbol = self.symbol_table.get(node.name)
            if symbol and symbol.type == 'vector':
                return symbol.size
        elif isinstance(node, AST.Vector):
            return len(node.elements)
        return None

    def get_matrix_size(self, node):
        if isinstance(node, AST.MatrixFunction):
            if node.name in ['eye', 'zeros', 'ones']:
                if len(node.params) == 1 and isinstance(node.params[0], AST.IntNum):
                    size = [node.params[0].value, node.params[0].value]
                    return size
                elif len(node.params) == 2 and all(isinstance(param, AST.IntNum) for param in node.params):
                    size = [node.params[0].value, node.params[1].value]
                    return size
        return None

    def get_variable_size(self, node):
        if isinstance(node, AST.Variable):
            symbol = self.symbol_table.get(node.name)
            if symbol and symbol.type == 'matrix' and hasattr(symbol, 'size'):
                return symbol.size
        return None

    def visit_BinExpr(self, node):

        left_type = self.visit(node.left)

        right_type = self.visit(node.right)
        if {left_type, right_type} == {"string", "int"} and node.op == "*":
            "ok"
        elif left_type != right_type and {left_type, right_type} != {"int", "float"}:
            self.report_error(
                f"Line {getattr(node, 'line', 'unknown')}: Type mismatch in binary operation '{node.op}': "
                f"'{left_type}' and '{right_type}' are not compatible.")
            return 'unknown'

        if left_type == 'vector' and right_type == 'vector':
            left_size = self.get_vector_size(node.left)
            right_size = self.get_vector_size(node.right)

            if left_size != right_size:
                self.report_error(
                    f"Line {getattr(node, 'line', 'unknown')}: Cannot perform operation '{node.op}' on vectors of different sizes: "
                    f"{left_size} and {right_size}.")
                return 'unknown'

        elif left_type == 'matrix' and right_type == 'matrix':
            left_size = self.get_variable_size(node.left)
            right_size = self.get_variable_size(node.right)

            if node.op == '*' and left_size[1] != right_size[0]:
                self.report_error(f"Line {getattr(node, 'line', 'unknown')}: "
                                  f"Cannot multiply matrices of shapes {left_size} and {right_size}.")
                return 'unknown'

            if node.op != "*" and left_size != right_size:
                self.report_error(
                    f"Line {getattr(node, 'line', 'unknown')}: Cannot perform operation '{node.op}' on matrices of different sizes: "
                    f"{left_size} and {right_size}.")
                return 'unknown'

        return left_type

    def visit_RelationExpr(self, node):

        left_type = self.visit(node.left)

        right_type = self.visit(node.right)

        if left_type != right_type:
            self.report_error(f"LINE {node.line}: Type mismatch in relational expression: "
                              f"'{left_type}' and '{right_type}' are not compatible for operation '{node.op}'.")

        if node.op not in ['==', '!=', '<', '<=', '>', '>=']:
            self.report_error(f"LINE {node.line}: Unsupported relational operator '{node.op}'.")

        return 'bool'

    def visit_UnaryExpr(self, node):

        value_type = self.visit(node.value)

        if node.op not in ['-', '!']:
            self.report_error(f"LINE {node.line}: Unsupported unary operator '{node.op}'.")

        if node.op == '-' and value_type not in ['int', 'float', 'matrix', 'vector']:
            self.report_error(f"LINE {node.line}: Unary '-' operator requires 'int' or 'float', got '{value_type}'.")
        elif node.op == '!' and value_type != 'bool':
            self.report_error(f"LINE {node.line}: Unary '!' operator requires 'bool', got '{value_type}'.")

        return value_type

    def visit_Transpose(self, node):

        value_type = self.visit(node.value)

        if value_type != 'matrix':
            self.report_error(f"LINE {node.line}: Transpose operation requires a matrix, got '{value_type}'.")

        return 'matrix'

    def visit_String(self, node):

        return 'string'

    def visit_Assignment(self, node):
        value_type = self.visit(node.value)

        # Get the variable from the symbol table
        id_symbol = self.symbol_table.get(node.id)
        if id_symbol is None:
            new_symbol = VariableSymbol(name=node.id, type=value_type)

            if value_type == 'int':
                new_symbol.size = 1
            elif value_type == 'vector':
                new_symbol.size = len(node.value.elements)
            elif value_type == 'matrix':
                new_symbol.size = self.get_matrix_size(node.value)

            self.symbol_table.put(node.id, new_symbol)
        else:
            if node.assign_type == '=':
                id_symbol.type = value_type
                if value_type == 'vector':
                    id_symbol.size = len(node.value.elements)
                elif value_type == 'matrix':
                    id_symbol.size = self.get_matrix_size(node.value)
            else:
                if id_symbol.type != value_type:
                    self.report_error(f"Line {node.line}: Type mismatch in compound assignment '{node.assign_type}': "
                                      f"'{id_symbol.type}' and '{value_type}' are not compatible.")

    def visit_AssignIndex(self, node):

        id_symbol = self.symbol_table.get(node.id)
        if id_symbol is None:
            self.report_error(f"LINE {node.line}: Variable '{node.id}' is not defined.")
            return

        if id_symbol.type not in ['array', 'matrix']:
            self.report_error(f"LINE {node.line}: Variable '{node.id}' is not indexable (type: '{id_symbol.type}').")
            return

        index_type = [self.visit(node.index)] if not isinstance(node.index, list) else [self.visit(idx) for idx in node.index]
        if any(map(lambda t: t != "int", index_type)):
            self.report_error(f"LINE {node.line}: Index must be of type 'int', got '{index_type}'.")

        value_type = self.visit(node.value)

        if node.assign_type not in ['=', '+=', '-=', '*=', '/=']:
            self.report_error(f"LINE {node.line}: Unsupported assignment operator '{node.assign_type}'.")
            return


    def visit_ForLoop(self, node):
        self.for_count += 1

        range_type = self.visit(node.range)

        if range_type != 'range':
            self.report_error(f"LINE {node.line}: For loop range must be of type 'range', got '{range_type}'.")

        scope = self.symbol_table.pushScope(f'for_{self.for_count}')
        self.symbol_table.put(scope.name, scope)
        scope.put(node.id, VariableSymbol(name=node.id, type='int'))
        self.symbol_table = scope

        self.in_loop += 1

        if node.instructions:
            self.visit(node.instructions)
        else:
            self.report_error(f"LINE {node.line}: Empty loop body in for loop.")

        self.in_loop -= 1

        self.symbol_table = scope.getParentScope()

    def visit_WhileLoop(self, node):
        self.while_count += 1
        condition_type = self.visit(node.condition)
        if condition_type != 'bool':
            self.report_error(f"LINE {node.line}: While loop condition must be of type 'bool', got '{condition_type}'.")

        self.in_loop += 1
        scope = self.symbol_table.pushScope(f'while_{self.while_count}')
        self.symbol_table.put(scope.name, scope)
        self.symbol_table = scope
        if node.instructions:
            self.visit(node.instructions)
        else:
            self.report_error(f"LINE {node.line}: Empty loop body in while loop.")

        self.in_loop -= 1
        self.symbol_table = scope.getParentScope()

    def visit_Vector(self, node):

        element_types = [self.visit(element) for element in node.elements]

        if len(set(element_types)) > 1:
            self.report_error(f"Line {node.line}: All elements in a vector must have the same type. "
                              f"Found types: {set(element_types)}.")

        if all(isinstance(element, AST.Vector) for element in node.elements):
            row_sizes = [len(element.elements) for element in node.elements]
            if len(set(row_sizes)) > 1:
                self.report_error(f"Line {node.line}: Matrix rows must have the same size. "
                                  f"Found row sizes: {row_sizes}.")
            return 'matrix'

        return 'vector'

    def visit_ArrayAccess(self, node):
        id_symbol = self.symbol_table.get(node.id)

        if id_symbol is None:
            self.report_error(f"Line {node.line}: Variable '{node.id}' is not defined.")
            return 'unknown'

        if id_symbol.type not in ['matrix', 'vector']:
            self.report_error(f"Line {node.line}: Variable '{node.id}' is not indexable (type: '{id_symbol.type}').")
            return 'unknown'

        matrix_size = id_symbol.size

        index_types = [self.visit(index) for index in node.indices]

        if any(itype != 'int' for itype in index_types):
            self.report_error(f"Line {node.line}: Array/matrix indices must be integers, got {index_types}.")
            return 'unknown'

        num_dimensions = len(matrix_size)
        num_indices = len(node.indices)

        if num_indices != num_dimensions:
            self.report_error(f"Line {node.line}: Matrix access requires {num_dimensions} indices, got {num_indices}.")
            return 'unknown'

        for i, index in enumerate(node.indices):
            index_value = index.value
            if index_value > matrix_size[i]:
                self.report_error(
                    f"Line {node.line}: Index {index_value} out of bounds for dimension {i + 1} of matrix with size {matrix_size}.")

        return 'unknown'

    def visit_Range(self, node):

        start_type = self.visit(node.start)

        end_type = self.visit(node.end)

        if start_type != 'int':
            self.report_error(f"LINE {node.line}: Range start must be of type 'int', got '{start_type}'.")
        if end_type != 'int':
            self.report_error(f"LINE {node.line}: Range end must be of type 'int', got '{end_type}'.")

        return 'range'

    def visit_MatrixFunction(self, node):

        param_values = [param.value if isinstance(param, AST.IntNum) else self.visit(param) for param in node.params]

        valid_functions = ['eye', 'zeros', 'ones']
        if node.name not in valid_functions:
            self.report_error(f"Line {node.line}: Unknown matrix function '{node.name}'.")
            return 'unknown'

        if node.name == 'eye':
            if len(param_values) == 1 and isinstance(param_values[0], int):
                return 'matrix'
            else:
                self.report_error(
                    f"Line {node.line}: 'eye' function requires one integer parameter, got {param_values}.")
        elif node.name in ['zeros', 'ones']:
            if len(param_values) == 1 and isinstance(param_values[0], int):
                return 'matrix'
            elif len(param_values) == 2 and all(isinstance(p, int) for p in param_values):
                return 'matrix'
            else:
                self.report_error(
                    f"Line {node.line}: '{node.name}' function requires one or two integer parameters, got {param_values}.")

        return 'unknown'

    def visit_Error(self, node):

        self.report_error(f"Line {node.line}: {node.message}")
