from lab3 import AST
from lab4.SymbolTable import SymbolTable, VariableSymbol
from printing import print_color
from collections import defaultdict

class NodeVisitor(object):

    def __init__(self):
        self.last_line = 0
        self.correct = True

    def report_error(self, message, line):
        self.correct = False
        if self.last_line == 0 :
            print_color("ERRORS:")
        line_str = f"    LINE {line}: "
        plural = 0
        if line != self.last_line :
            print_color(line_str, end = "")
        else : plural = 1
        print_color(" "*plural*len(line_str) + message, color = "f54d30")
        self.last_line = line
        
    def visit_first(self, node) :
        self.visit(node)
    
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
    
    def visit(self, node):
        if node is None:
            # print("Visited: None")
            return
        # if not isinstance(node, list):
        #     print(f"Visiting node: {type(node).__name__}, line: {getattr(node, 'line', 'unknown')}")

        try:
            return super().visit(node)
        except Exception as e:
            line = getattr(node, 'line', 'unknown')
            self.report_error(f"{str(e)}", line)

    def visit_CompoundStatement(self, node):
        if not node.instructions:
            self.report_error(f"Empty compound statement.", node.line)
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
            self.report_error(f"Missing instructions in 'if' block.", node.line)

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
            self.report_error(f"Missing value in 'print' instruction.", node.line)
        else:
            self.visit(node.value)

    def visit_ReturnInstruction(self, node):
        if node.value is not None:
            self.visit(node.value)
        else:
            self.report_error(f"'return' statement with no value.", node.line)

    def visit_BreakInstruction(self, node):
        if self.in_loop == 0:
            self.report_error(f"'break' statement used outside of a loop.", node.line)

    def visit_ContinueInstruction(self, node):
        if self.in_loop == 0:
            self.report_error(f"'continue' statement used outside of a loop.", node.line)

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_Variable(self, node):

        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.report_error(f"Variable '{node.name}' is not defined.", node.line)
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

        if left_type != right_type:
            self.report_error(
                f"Type mismatch in binary operation '{node.op}': "
                f"'{left_type}' and '{right_type}' are not compatible.", getattr(node, 'line', 'unknown'))
            return 'unknown'

        if left_type == 'vector' and right_type == 'vector':
            left_size = self.get_vector_size(node.left)
            right_size = self.get_vector_size(node.right)

            if left_size != right_size:
                self.report_error(
                    f"Cannot perform operation '{node.op}' on vectors of different sizes: "
                    f"{left_size} and {right_size}.", getattr(node, 'line', 'unknown'))
                return 'unknown'

        elif left_type == 'matrix' and right_type == 'matrix':
            left_size = self.get_variable_size(node.left)
            right_size = self.get_variable_size(node.right)

            if node.op == '*' and left_size[1] != right_size[0]:
                self.report_error(f"Cannot multiply matrices of shapes {left_size} and {right_size}.", getattr(node, 'line', 'unknown'))
                return 'unknown'

            if node.op != "*" and left_size != right_size:
                self.report_error(
                    f"Cannot perform operation '{node.op}' on matrices of different sizes: "
                    f"{left_size} and {right_size}.", getattr(node, 'line', 'unknown'))
                return 'unknown'

        return left_type

    def visit_RelationExpr(self, node):

        left_type = self.visit(node.left)

        right_type = self.visit(node.right)

        if left_type != right_type:
            self.report_error("Type mismatch in relational expression: "
                              f"'{left_type}' and '{right_type}' are not compatible for operation '{node.op}'.", node.line)

        if node.op not in ['==', '!=', '<', '<=', '>', '>=']:
            self.report_error(f"Unsupported relational operator '{node.op}'.")

        return 'bool'

    def visit_UnaryExpr(self, node):

        value_type = self.visit(node.value)

        if node.op not in ['-', '!']:
            self.report_error(f"Unsupported unary operator '{node.op}'.", node.line)

        if node.op == '-' and value_type not in ['int', 'float']:
            self.report_error(f"Unary '-' operator requires 'int' or 'float', got '{value_type}'.", node.line)
        elif node.op == '!' and value_type != 'bool':
            self.report_error(f"Unary '!' operator requires 'bool', got '{value_type}'.", node.line)

        return value_type

    def visit_Transpose(self, node):

        value_type = self.visit(node.value)

        if value_type != 'matrix':
            self.report_error(f"Transpose operation requires a matrix, got '{value_type}'.", node.line)

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
                    self.report_error(f"Type mismatch in compound assignment '{node.assign_type}': "
                                      f"'{id_symbol.type}' and '{value_type}' are not compatible.", node.line)

    def visit_AssignIndex(self, node):

        id_symbol = self.symbol_table.get(node.id)
        if id_symbol is None:
            self.report_error(f"Variable '{node.id}' is not defined.", node.line)
            return

        if id_symbol.type not in ['array', 'matrix']:
            self.report_error(f"Variable '{node.id}' is not indexable (type: '{id_symbol.type}').", node.line)
            return

        index_type = self.visit(node.index)
        if index_type != 'int':
            self.report_error(f"Index must be of type 'int', got '{index_type}'.", node.line)

        value_type = self.visit(node.value)

        if node.assign_type not in ['=', '+=', '-=', '*=', '/=']:
            self.report_error(f"Unsupported assignment operator '{node.assign_type}'.", node.line)
            return

        element_type = id_symbol.element_type if hasattr(id_symbol, 'element_type') else id_symbol.type
        if node.assign_type == '=' and element_type != value_type:
            self.report_error(f"Type mismatch in indexed assignment: "
                              f"cannot assign '{value_type}' to '{element_type}' in '{node.id}'.", node.line)
        elif node.assign_type != '=' and element_type != value_type:
            self.report_error(f"Type mismatch in compound indexed assignment '{node.assign_type}': "
                              f"'{element_type}' and '{value_type}' are not compatible.", node.line)

    def visit_ForLoop(self, node):
        self.for_count += 1

        range_type = self.visit(node.range)

        if range_type != 'range':
            self.report_error(f"For loop range must be of type 'range', got '{range_type}'.", node.line)

        scope = self.symbol_table.pushScope(f'for_{self.for_count}')
        self.symbol_table.put(scope.name, scope)
        scope.put(node.id, VariableSymbol(name=node.id, type='int'))
        self.symbol_table = scope

        self.in_loop += 1

        if node.instructions:
            self.visit(node.instructions)
        else:
            self.report_error(f"Empty loop body in for loop.", node.line)

        self.in_loop -= 1

        self.symbol_table = scope.getParentScope()

    def visit_WhileLoop(self, node):
        self.while_count += 1
        condition_type = self.visit(node.condition)
        if condition_type != 'bool':
            self.report_error(f"While loop condition must be of type 'bool', got '{condition_type}'.", node.line)

        self.in_loop += 1
        scope = self.symbol_table.pushScope(f'while_{self.while_count}')
        self.symbol_table.put(scope.name, scope)
        self.symbol_table = scope
        if node.instructions:
            self.visit(node.instructions)
        else:
            self.report_error(f"Empty loop body in while loop.", node.line)

        self.in_loop -= 1
        self.symbol_table = scope.getParentScope()

    def visit_Vector(self, node):

        element_types = [self.visit(element) for element in node.elements]

        if len(set(element_types)) > 1:
            self.report_error(f"All elements in a vector must have the same type. "
                              f"Found types: {set(element_types)}.", node.line)

        if all(isinstance(element, AST.Vector) for element in node.elements):
            row_sizes = [len(element.elements) for element in node.elements]
            if len(set(row_sizes)) > 1:
                self.report_error(f"Matrix rows must have the same size. "
                                  f"Found row sizes: {row_sizes}.", node.line)
            return 'matrix'

        return 'vector'

    def visit_ArrayAccess(self, node):
        id_symbol = self.symbol_table.get(node.id)

        if id_symbol is None:
            self.report_error(f"Variable '{node.id}' is not defined.", node.line)
            return 'unknown'

        if id_symbol.type not in ['matrix', 'vector']:
            self.report_error(f"Variable '{node.id}' is not indexable (type: '{id_symbol.type}').", node.line)
            return 'unknown'

        matrix_size = id_symbol.size

        index_types = [self.visit(index) for index in node.indices]

        if any(itype != 'int' for itype in index_types):
            self.report_error(f"Array/matrix indices must be integers, got {index_types}.", node.line)
            return 'unknown'

        num_dimensions = len(matrix_size)
        num_indices = len(node.indices)

        if num_indices != num_dimensions:
            self.report_error(f"Matrix access requires {num_dimensions} indices, got {num_indices}.", node.line)
            return 'unknown'

        for i, index in enumerate(node.indices):
            index_value = index.value
            if index_value > matrix_size[i]:
                self.report_error(
                    f"Index {index_value} out of bounds for dimension {i + 1} of matrix with size {matrix_size}.", node.line)

        return 'unknown'

    def visit_Range(self, node):

        start_type = self.visit(node.start)

        end_type = self.visit(node.end)

        if start_type != 'int':
            self.report_error(f"Range start must be of type 'int', got '{start_type}'.", node.line)
        if end_type != 'int':
            self.report_error(f"Range end must be of type 'int', got '{end_type}'.", node.line)

        return 'range'

    def visit_MatrixFunction(self, node):

        param_values = [param.value if isinstance(param, AST.IntNum) else self.visit(param) for param in node.params]

        valid_functions = ['eye', 'zeros', 'ones']
        if node.name not in valid_functions:
            self.report_error(f"Unknown matrix function '{node.name}'.", node.line)
            return 'unknown'

        if node.name == 'eye':
            if len(param_values) == 1 and isinstance(param_values[0], int):
                return 'matrix'
            else:
                self.report_error(
                    f"'eye' function requires one integer parameter, got {param_values}.", node.line)
        elif node.name in ['zeros', 'ones']:
            if len(param_values) == 1 and isinstance(param_values[0], int):
                return 'matrix'
            elif len(param_values) == 2 and all(isinstance(p, int) for p in param_values):
                return 'matrix'
            else:
                self.report_error(
                    f"'{node.name}' function requires one or two integer parameters, got {param_values}.", node.line)

        return 'unknown'

    def visit_Error(self, node):

        self.report_error(f"{node.message}", node.line)