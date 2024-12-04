from lab3 import AST
from lab4.SymbolTable import SymbolTable, VariableSymbol

class NodeVisitor(object):

    def __init__(self) :
        self.errors = []

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


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
        self.errors = []
        self.in_loop = 0
        self.symbol_table = SymbolTable()

    def report_error(self, message):
        print(f"ERROR IN {message}")
        self.errors.append(message)

    def visit(self, node):
        if node is None:
            print("Visited: None")
            return
        print(f"Visiting node: {type(node).__name__}, line: {getattr(node, 'line', 'unknown')}")
        try:
            return super().visit(node)
        except Exception as e:
            line = getattr(node, 'line', 'unknown')
            self.report_error(f"LINE {line}: {str(e)}")

    def visit_CompoundStatement(self, node):
        print(f"DEBUG: Visiting CompoundStatement at line {node.line}")
        if not node.instructions:
            self.report_error(f"LINE {node.line}: Empty compound statement.")
            return
        for instruction in node.instructions:
            self.visit(instruction)



    def visit_ConditionalInstruction(self, node):
        print(f"DEBUG: Visiting ConditionalInstruction at line {node.line}")
        self.visit(node.condition)
        if node.instructions:
            self.visit(node.instructions)
        else:
            self.report_error(f"LINE {node.line}: Missing instructions in 'if' block.")
        if node.else_instruction:
            self.visit(node.else_instruction)




    def visit_PrintInstruction(self, node):
        print(f"DEBUG: Visiting PrintInstruction at line {node.line}, value: {node.value}")
        if node.value is None:
            self.report_error(f"LINE {node.line}: Missing value in 'print' instruction.")
        else:
            self.visit(node.value)



    def visit_ReturnInstruction(self, node):
        print(f"DEBUG: Visiting ReturnInstruction at line {node.line}, value: {node.value}")
        if node.value is not None:
            self.visit(node.value)
        else:
            self.report_error(f"LINE {node.line}: 'return' statement with no value.")





    def visit_BreakInstruction(self, node):
        print(f"DEBUG: Visiting BreakInstruction at line {node.line}")
        if self.in_loop == 0:
            self.report_error(f"LINE {node.line}: 'break' statement used outside of a loop.")




    def visit_ContinueInstruction(self, node):
        print(f"DEBUG: Visiting ContinueInstruction at line {node.line}")
        if self.in_loop == 0:
            self.report_error(f"LINE {node.line}: 'continue' statement used outside of a loop.")






    def visit_IntNum(self, node):
        print(f"DEBUG: Visiting IntNum with value {node.value} at line {node.line}")
        return "int"




    def visit_FloatNum(self, node):
        print(f"DEBUG: Visiting FloatNum with value {node.value} at line {node.line}")
        return "float"

    def visit_Variable(self, node):
        print(f"DEBUG: Visiting Variable with name '{node.name}' at line {node.line}")
        
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.report_error(f"Line {node.line}: Variable '{node.name}' is not defined.")
            return None
        print(f"DEBUG: Variable '{node.name}' has type '{symbol.type}' and size '{getattr(symbol, 'size', None)}'.")
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
                    print(f"DEBUG: Matrix size determined as {size}")
                    return size
                elif len(node.params) == 2 and all(isinstance(param, AST.IntNum) for param in node.params):
                    size = [node.params[0].value, node.params[1].value]
                    print(f"DEBUG: Matrix size determined as {size}")
                    return size
        return None


    def get_variable_size(self, node):
        if isinstance(node, AST.Variable):
            symbol = self.symbol_table.get(node.name)
            if symbol and symbol.type == 'matrix' and hasattr(symbol, 'size'):
                return symbol.size
        return None




    def visit_BinExpr(self, node):
        print(f"DEBUG: Visiting BinExpr with operator '{node.op}' at line {getattr(node, 'line', 'unknown')}")
        
        left_type = self.visit(node.left)
        print(f"DEBUG: Left operand type: {left_type}")
        
        right_type = self.visit(node.right)
        print(f"DEBUG: Right operand type: {right_type}")
        
        if left_type != right_type:
            self.report_error(f"Line {getattr(node, 'line', 'unknown')}: Type mismatch in binary operation '{node.op}': "
                            f"'{left_type}' and '{right_type}' are not compatible.")
            return 'unknown'
        
        if left_type == 'vector' and right_type == 'vector':
            left_size = self.get_vector_size(node.left)
            right_size = self.get_vector_size(node.right)
            print(f"DEBUG: Left vector size: {left_size}, Right vector size: {right_size}")
            
            if left_size != right_size:
                self.report_error(f"Line {getattr(node, 'line', 'unknown')}: Cannot perform operation '{node.op}' on vectors of different sizes: "
                                f"{left_size} and {right_size}.")
                return 'unknown'
        
        elif left_type == 'matrix' and right_type == 'matrix':
            left_size = self.get_variable_size(node.left)
            right_size = self.get_variable_size(node.right)
            print(f"DEBUG: Left matrix size: {left_size}, Right matrix size: {right_size}")
            
            if left_size != right_size:
                self.report_error(f"Line {getattr(node, 'line', 'unknown')}: Cannot perform operation '{node.op}' on matrices of different sizes: "
                                f"{left_size} and {right_size}.")
                return 'unknown'
        
        return left_type

    def visit_RelationExpr(self, node):
        print(f"DEBUG: Visiting RelationExpr with operator '{node.op}' at line {node.line}")
        
        left_type = self.visit(node.left)
        print(f"DEBUG: Left operand type: {left_type}")
        
        right_type = self.visit(node.right)
        print(f"DEBUG: Right operand type: {right_type}")
        
        if left_type != right_type:
            self.report_error(f"LINE {node.line}: Type mismatch in relational expression: "
                            f"'{left_type}' and '{right_type}' are not compatible for operation '{node.op}'.")
        
        if node.op not in ['==', '!=', '<', '<=', '>', '>=']:
            self.report_error(f"LINE {node.line}: Unsupported relational operator '{node.op}'.")
        
        return 'bool'


    def visit_UnaryExpr(self, node):
        print(f"DEBUG: Visiting UnaryExpr with operator '{node.op}' at line {node.line}")
        
        value_type = self.visit(node.value)
        print(f"DEBUG: Operand type: {value_type}")
        
        if node.op not in ['-', '!']:
            self.report_error(f"LINE {node.line}: Unsupported unary operator '{node.op}'.")
        
        if node.op == '-' and value_type not in ['int', 'float']:
            self.report_error(f"LINE {node.line}: Unary '-' operator requires 'int' or 'float', got '{value_type}'.")
        elif node.op == '!' and value_type != 'bool':
            self.report_error(f"LINE {node.line}: Unary '!' operator requires 'bool', got '{value_type}'.")
        
        return value_type


    def visit_Transpose(self, node):
        print(f"DEBUG: Visiting Transpose at line {node.line}")
        
        value_type = self.visit(node.value)
        print(f"DEBUG: Operand type for transpose: {value_type}")
        
        if value_type != 'matrix':
            self.report_error(f"LINE {node.line}: Transpose operation requires a matrix, got '{value_type}'.")
        
        return 'matrix'



    def visit_String(self, node):
        print(f"DEBUG: Visiting String with value '{node.value}' at line {node.line}")
        
        return 'string'



    def visit_Assignment(self, node):
        print(f"DEBUG: Visiting Assignment at line {node.line}")
        print(f"DEBUG: Variable ID: {node.id}, Assignment type: '{node.assign_type}'")
        
        value_type = self.visit(node.value)
        print(f"DEBUG: Value type: {value_type}")
        
        # Get the variable from the symbol table
        id_symbol = self.symbol_table.get(node.id)
        if id_symbol is None:
            new_symbol = VariableSymbol(name=node.id, type=value_type)
            
            if value_type == 'int':
                print(f"DEBUG: Variable '{node.id}' created with type '{value_type}'.")
            elif value_type == 'vector':
                new_symbol.size = len(node.value.elements)
                print(f"DEBUG: Variable '{node.id}' created with type '{value_type}' and size '{new_symbol.size}'.")
            elif value_type == 'matrix':
                new_symbol.size = self.get_matrix_size(node.value)
                print(f"DEBUG: Variable '{node.id}' created with type '{value_type}' and size '{new_symbol.size}'.")
            
            self.symbol_table.put(node.id, new_symbol)
        else:
            if node.assign_type == '=':
                print(f"DEBUG: Reassigning variable '{node.id}' from type '{id_symbol.type}' to '{value_type}'.")
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
        print(f"DEBUG: Visiting AssignIndex at line {node.line}")
        print(f"DEBUG: Variable ID: {node.id}, Index: {node.index}, Assignment type: '{node.assign_type}'")
        
        id_symbol = self.symbol_table.get(node.id)
        if id_symbol is None:
            self.report_error(f"LINE {node.line}: Variable '{node.id}' is not defined.")
            return

        if id_symbol.type not in ['array', 'matrix']:
            self.report_error(f"LINE {node.line}: Variable '{node.id}' is not indexable (type: '{id_symbol.type}').")
            return

        index_type = self.visit(node.index)
        print(f"DEBUG: Index type: {index_type}")
        if index_type != 'int':
            self.report_error(f"LINE {node.line}: Index must be of type 'int', got '{index_type}'.")

        value_type = self.visit(node.value)
        print(f"DEBUG: Value type: {value_type}")

        if node.assign_type not in ['=', '+=', '-=', '*=', '/=']:
            self.report_error(f"LINE {node.line}: Unsupported assignment operator '{node.assign_type}'.")
            return

        element_type = id_symbol.element_type if hasattr(id_symbol, 'element_type') else id_symbol.type
        if node.assign_type == '=' and element_type != value_type:
            self.report_error(f"LINE {node.line}: Type mismatch in indexed assignment: "
                            f"cannot assign '{value_type}' to '{element_type}' in '{node.id}'.")
        elif node.assign_type != '=' and element_type != value_type:
            self.report_error(f"LINE {node.line}: Type mismatch in compound indexed assignment '{node.assign_type}': "
                            f"'{element_type}' and '{value_type}' are not compatible.")


    def visit_ForLoop(self, node):
        print(f"DEBUG: Visiting ForLoop at line {node.line}")
        print(f"DEBUG: Loop variable ID: {node.id}")
        
        range_type = self.visit(node.range)
        print(f"DEBUG: Range type: {range_type}")
        if range_type != 'range':
            self.report_error(f"LINE {node.line}: For loop range must be of type 'range', got '{range_type}'.")

        self.in_loop += 1
        print(f"DEBUG: Entering loop context, in_loop count: {self.in_loop}")

        if node.instructions:
            self.visit(node.instructions)
        else:
            self.report_error(f"LINE {node.line}: Empty loop body in for loop.")
        
        self.in_loop -= 1
        print(f"DEBUG: Exiting loop context, in_loop count: {self.in_loop}")



    def visit_WhileLoop(self, node):
        print(f"DEBUG: Visiting WhileLoop at line {node.line}")
        
        condition_type = self.visit(node.condition)
        print(f"DEBUG: Condition type: {condition_type}")
        if condition_type != 'bool':
            self.report_error(f"LINE {node.line}: While loop condition must be of type 'bool', got '{condition_type}'.")
        
        self.in_loop += 1
        print(f"DEBUG: Entering loop context, in_loop count: {self.in_loop}")

        if node.instructions:
            self.visit(node.instructions)
        else:
            self.report_error(f"LINE {node.line}: Empty loop body in while loop.")
        
        self.in_loop -= 1
        print(f"DEBUG: Exiting loop context, in_loop count: {self.in_loop}")


    def visit_Vector(self, node):
        print(f"DEBUG: Visiting Vector at line {node.line}")
        print(f"DEBUG: Vector elements count: {len(node.elements)}")
        
        element_types = [self.visit(element) for element in node.elements]
        print(f"DEBUG: Element types in vector: {element_types}")
        
        if len(set(element_types)) > 1:
            self.report_error(f"Line {node.line}: All elements in a vector must have the same type. "
                            f"Found types: {set(element_types)}.")
        
        if all(isinstance(element, AST.Vector) for element in node.elements):
            row_sizes = [len(element.elements) for element in node.elements]
            print(f"DEBUG: Row sizes for potential matrix: {row_sizes}")
            if len(set(row_sizes)) > 1:
                self.report_error(f"Line {node.line}: Matrix rows must have the same size. "
                                f"Found row sizes: {row_sizes}.")
            return 'matrix'
        
        return 'vector'






    def visit_ArrayAccess(self, node):
        print(f"DEBUG: Visiting ArrayAccess at line {node.line}")
        id_symbol = self.symbol_table.get(node.id)
        
        if id_symbol is None:
            self.report_error(f"Line {node.line}: Variable '{node.id}' is not defined.")
            return 'unknown'

        if id_symbol.type not in ['matrix', 'vector']:
            self.report_error(f"Line {node.line}: Variable '{node.id}' is not indexable (type: '{id_symbol.type}').")
            return 'unknown'

        matrix_size = id_symbol.size
        print(f"DEBUG: {node.id} size: {matrix_size}")

        index_types = [self.visit(index) for index in node.indices]
        print(f"DEBUG: Index types: {index_types}")
        
        if not all(itype == 'int' for itype in index_types):
            self.report_error(f"Line {node.line}: Array/matrix indices must be integers, got {index_types}.")
            return 'unknown'

        num_dimensions = len(matrix_size)
        num_indices = len(node.indices)
        print(f"DEBUG: Number of dimensions: {num_dimensions}, Number of indices: {num_indices}")

        if num_indices != num_dimensions:
            self.report_error(f"Line {node.line}: Matrix access requires {num_dimensions} indices, got {num_indices}.")
            return 'unknown'
        
        for i, index in enumerate(node.indices):
            index_value = index.value
            if index_value > matrix_size[i]:
                self.report_error(f"Line {node.line}: Index {index_value} out of bounds for dimension {i + 1} of matrix with size {matrix_size}.")

        return 'unknown'




    def visit_Range(self, node):
        print(f"DEBUG: Visiting Range at line {node.line}")
        
        start_type = self.visit(node.start)
        print(f"DEBUG: Start type: {start_type}")
        
        end_type = self.visit(node.end)
        print(f"DEBUG: End type: {end_type}")
        
        if start_type != 'int':
            self.report_error(f"LINE {node.line}: Range start must be of type 'int', got '{start_type}'.")
        if end_type != 'int':
            self.report_error(f"LINE {node.line}: Range end must be of type 'int', got '{end_type}'.")
        
        return 'range'



    def visit_MatrixFunction(self, node):
        print(f"DEBUG: Visiting MatrixFunction '{node.name}' at line {node.line}")
        
        param_values = [param.value if isinstance(param, AST.IntNum) else self.visit(param) for param in node.params]
        print(f"DEBUG: Parameter values: {param_values}")
        
        valid_functions = ['eye', 'zeros', 'ones']
        if node.name not in valid_functions:
            self.report_error(f"Line {node.line}: Unknown matrix function '{node.name}'.")
            return 'unknown'
        
        if node.name == 'eye':
            if len(param_values) == 1 and isinstance(param_values[0], int):
                print(f"DEBUG: 'eye' creates a square matrix of size {param_values[0]}x{param_values[0]}")
                return 'matrix'
            else:
                self.report_error(f"Line {node.line}: 'eye' function requires one integer parameter, got {param_values}.")
        elif node.name in ['zeros', 'ones']:
            if len(param_values) == 1 and isinstance(param_values[0], int):
                return 'matrix'
            elif len(param_values) == 2 and all(isinstance(p, int) for p in param_values):
                return 'matrix'
            else:
                self.report_error(f"Line {node.line}: '{node.name}' function requires one or two integer parameters, got {param_values}.")
        
        return 'unknown'





    def visit_Error(self, node):
        print(f"DEBUG: Visiting Error at line {node.line}")
        print(f"DEBUG: Error message: {node.message}")
        
        self.report_error(f"Line {node.line}: {node.message}")
