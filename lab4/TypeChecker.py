from lab3 import AST
from lab4.SymbolTable import SymbolTable, VariableSymbol
from printing import print_color
from tokens_names import *
from util import get_matrix_shape

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
        super().__init__()
        self.in_loop = 0

        self.for_count = 0
        self.while_count = 0
        self.if_count = 0
        self.else_count = 0


        self.symbol_table = SymbolTable()
    
    def visit(self, node):
        if node is None:
            # # print("Visited: None")
            return
        # if not isinstance(node, list):
        #     # print(f"Visiting node: {type(node).__name__}, line: {getattr(node, 'line', UNKNOWN)}")

        try:
            return super().visit(node)
        except Exception as e:
            line = getattr(node, 'line', UNKNOWN)
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
            self.report_error(f"Missing instructions in {IF} block.", node.line)

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
            self.report_error(f"Missing value in {PRINT} instruction.", node.line)
        else:
            self.visit(node.value)

    def visit_ReturnInstruction(self, node):
        if node.value is not None:
            self.visit(node.value)
        else:
            self.report_error(f"{RETURN} statement with no value.", node.line)

    def visit_BreakInstruction(self, node):
        if self.in_loop == 0:
            self.report_error(f"{BREAK} statement used outside of a loop.", node.line)

    def visit_ContinueInstruction(self, node):
        if self.in_loop == 0:
            self.report_error(f"{CONTINUE} statement used outside of a loop.", node.line)

    def visit_Variable(self, node):
        # print(node)
        
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.report_error(f"Variable '{node.name}' is not defined.", node.line)
            return None
        return symbol.type

    def visit_IntNum(self, node):
        return INTNUM

    def visit_FloatNum(self, node):
        return FLOATNUM

    def get_matrix_size(self, node):
        if isinstance(node, AST.MatrixFunction):
            if node.name in [EYE, ZEROS, ONES]:
                if isinstance(node.params[0], AST.Variable) :
                    node.params = [self.symbol_table.get(param.name).value for param in node.params]
                if len(node.params) == 1 and isinstance(node.params[0], AST.IntNum) or node.params[0] == INTNUM:
                    if node.name != EYE :
                        size = [1, node.params[0].value]
                    else :
                        size = [node.params[0].value, node.params[0].value]
                    return size
                elif len(node.params) == 2 and all(isinstance(param, AST.IntNum) or param == INTNUM for param in node.params):
                    size = [node.params[0].value, node.params[1].value]
                    return size
        elif isinstance(node, AST.Matrix) :
            size = get_matrix_shape(node)
            if len(size) == 1 : size = [1] + size
            return size
        elif isinstance(node, AST.BinExpr) :
            left_size = self.get_variable_size(node.left)
            right_size = self.get_variable_size(node.right)
            size = left_size
            if node.op == TIMES :
                size = [left_size[0], right_size[1]]
            elif node.op == DIVIDE :
                size = [right_size[1], left_size[1]]
            return size
        return None

    def get_variable_size(self, node):
        if isinstance(node, AST.Variable):
            symbol = self.symbol_table.get(node.name)
            if symbol and hasattr(symbol, 'size'):
                if symbol.size is None : symbol.size = 1
                return symbol.size
            if symbol :
                return 1
        elif isinstance(node, AST.String) or isinstance(node, AST.IntNum) or isinstance(node, AST.FloatNum) :
            return 1
        elif isinstance(node, AST.BinExpr) :
            return max(self.get_variable_size(node.left), self.get_variable_size(node.right))
        else :
            symbol = self.symbol_table.get(node)
            return symbol.size
        return None

    def visit_BinExpr(self, node):
        
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        op_type = node.op
        
        # print(f"Type compatibility check for {left_type} and {right_type}")
        if not compatible(left_type, right_type, op_type) :
            self.report_error(
                f"Type mismatch in binary operation '{node.op.symbol}': "
                f"'{left_type}' and '{right_type}' are not compatible.", getattr(node, 'line', UNKNOWN))
            return UNKNOWN
        # print("Compatible")
        left_size = self.get_variable_size(node.left)
        right_size = self.get_variable_size(node.right)
        # print(left_size, right_size)
        
        if ((left_type == right_type == MATRIX) and 
                ((op_type == TIMES and left_size[1] != right_size[0]) or
                (op_type == DIVIDE and left_size[0] != right_size[0]) or
                (op_type in [PLUS, MINUS] and left_size != right_size))) :
                self.report_error(f"Cannot execute operation '{op_type.symbol}' on matrices of shapes {left_size} and {right_size}.", getattr(node, 'line', UNKNOWN))
                return UNKNOWN
        # print("Operation can be executed")
        
        if (MATRIX in (left_type, right_type)) :
            return MATRIX
        elif (FLOATNUM in (left_type, right_type)) :
            return FLOATNUM
        else : 
            return INTNUM

    def visit_RelationExpr(self, node):

        left_type = self.visit(node.left)

        right_type = self.visit(node.right)

        if left_type != right_type:
            self.report_error("Type mismatch in relational expression: "
                              f"'{left_type}' and '{right_type}' are not compatible for operation '{node.op}'.", node.line)

        if node.op not in [EQ, NEQ, LT, LTE, GT, GTE] :
            self.report_error(f"Unsupported relational operator '{node.op}'.")

        return BOOL

    def visit_UnaryExpr(self, node):

        value_type = self.visit(node.value)

        if node.op != UMINUS :
            self.report_error(f"Unsupported unary operator '{node.op}'.", node.line)

        if node.op == UMINUS and value_type in [STRING] :
            self.report_error(f"{UMINUS} operator won't work with '{value_type}'.", node.line)
        # print(node)
        return value_type

    def visit_Transpose(self, node):

        value_type = self.visit(node.value)

        if value_type != MATRIX:
            self.report_error(f"{TRANSPOSE} operation requires a {MATRIX} object, got '{value_type}'.", node.line)

        return MATRIX

    def visit_String(self, node):
        return STRING
    
    def visit_Matrix(self, node) :
        elements = node.elements
        element_types = set([self.visit(element) for element in elements])
        
        if len(element_types) > 1 and not (INTNUM in element_types and FLOATNUM in element_types) :
            self.report_error(f"All elements in a matrix must have the same (or correlating) type. "
                              f"Found types: {set(element_types)}.", node.line)

        
        if all(isinstance(element, AST.Matrix) for element in node.elements):
            row_sizes = [len(element.elements) for element in node.elements]
            if len(set(row_sizes)) > 1 :
                self.report_error(f"Matrix rows must have the same size. "
                                  f"Found row sizes: {row_sizes}.", node.line)
                return UNKNOWN

        return MATRIX

    def visit_Assignment(self, node) :
        
        value_type = self.visit(node.value)
        id_symbol = self.symbol_table.get(node.id)
        assign_type = node.assign_type
        
        # print(node)
        
        if id_symbol is None:
            new_symbol = VariableSymbol(name=node.id, type=value_type)
            # print(node.value)
            if value_type != MATRIX:
                new_symbol.size = 1
                new_symbol.value = node.value
            else:
                # print("sending to get matrix size")
                new_symbol.size = self.get_matrix_size(node.value)
                # print(new_symbol.size)
            if isinstance(node.value, AST.MatrixFunction) :
                new_symbol.dtype = FLOATNUM
            elif isinstance(node.value, AST.Matrix) :
                try :
                    value = node.value.elements[0].elements[0]
                except :
                    value = node.value.elements[0]
                new_symbol.dtype = self.visit(value)
            elif isinstance(node.value, AST.UnaryExpr) :
                # print(node.value.value)
                # print(self.symbol_table.get(node.value.value.name))
                new_symbol.size = self.symbol_table.get(node.value.value.name).size
            if new_symbol.dtype is None : new_symbol.dtype = FLOATNUM
            self.symbol_table.put(node.id, new_symbol)
            # print(new_symbol)
            
        else:
            if assign_type == ASSIGN :
                id_symbol.type = value_type
                if value_type == MATRIX:
                    id_symbol.size = self.get_matrix_size(node.value)
                else :
                    id_symbol.size = 1
            else:
                if id_symbol.type != value_type:
                    self.report_error(f"Type mismatch in compound assignment '{node.assign_type}': "
                                      f"'{id_symbol.type}' and '{value_type}' are not compatible.", node.line)

            # print(id_symbol)
        

    def visit_ForLoop(self, node):
        self.for_count += 1
        
        range_type = self.visit(node.range)

        if range_type != RANGE:
            self.report_error(f"For loop range must be of type '{RANGE}', got '{range_type}'.", node.line)

        scope = self.symbol_table.pushScope(f'for_{self.for_count}')
        self.symbol_table.put(scope.name, scope)
        scope.put(node.id, VariableSymbol(name=node.id, type=INTNUM))
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
        if condition_type != BOOL:
            self.report_error(f"While loop condition must be of type '{BOOL}', got '{condition_type}'.", node.line)

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

    def visit_AssignIndex(self, node):
        id_symbol = self.symbol_table.get(node.id)
        if id_symbol is None:
            self.report_error(f"Variable '{node.id}' is not defined.", node.line)
            return UNKNOWN

        if id_symbol.type != MATRIX :
            self.report_error(f"Variable '{node.id}' is not indexable (type: '{id_symbol.type}').", node.line)
            return UNKNOWN
        index_types = set([self.visit(ind) for ind in node.index])
        if len(index_types) > 1 :
            self.report_error(f"All indexes must be of the same type, instead got: {index_types}", node.line)
            return UNKNOWN
        index_type = list(index_types)[0]
        if index_type not in  [INTNUM, RANGE] :
            self.report_error(f"Index must be of type {INTNUM} or {RANGE}, got '{index_type}'.", node.line)
            return UNKNOWN


        if node.assign_type not in [ASSIGN, ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN]:
            self.report_error(f"Unsupported assignment operator '{node.assign_type}'.", node.line)
            return UNKNOWN

        value_type = self.visit(node.value)
        
        variable_size = self.get_variable_size(node.id)
        
        variable_type = self.symbol_table.get(node.id).dtype
        if len(node.index) > len(variable_size) :
            self.report_error(f"Unable to read {node.index} from {node.id} -> Index too long.", node.line)
            return UNKNOWN
        elif len(node.index) == len(variable_size) :
            if (not variable_type in [INTNUM, FLOATNUM] or not value_type in [INTNUM, FLOATNUM]) and (variable_type != value_type) :
                self.report_error(f"Unable to insert {value_type} into {variable_type}-typed matrix.", node.line)
        else :
            if value_type != MATRIX or self.get_matrix_size(node.value) != [1, variable_size[len(node.index)]] :
                self.report_error("Mismatched types", node.line)
                    

    def visit_MatrixAccess(self, node):
        id_symbol = self.symbol_table.get(node.id)

        if id_symbol is None:
            self.report_error(f"Variable '{node.id}' is not defined.", node.line)
            return UNKNOWN

        if id_symbol.type != MATRIX :
            self.report_error(f"Variable '{node.id}' is not indexable (type: '{id_symbol.type}').", node.line)
            return UNKNOWN

        matrix_size = id_symbol.size

        index_types = [self.visit(index) for index in node.indices]

        if any(itype != INTNUM for itype in index_types):
            self.report_error(f"Matrix indices must be integers, got {index_types}.", node.line)
            return UNKNOWN

        num_dimensions = len(matrix_size)
        num_indices = len(node.indices)

        if num_indices != num_dimensions:
            self.report_error(f"Matrix access requires {num_dimensions} indices, got {num_indices}.", node.line)
            return UNKNOWN

        for i, index in enumerate(node.indices):
            index_value = index.value
            if index_value > matrix_size[i]:
                self.report_error(
                    f"Index {index_value} out of bounds for dimension {i + 1} of matrix with size {matrix_size}.", node.line)

        return UNKNOWN

    def visit_Range(self, node):

        start_type = self.visit(node.start)

        end_type = self.visit(node.end)

        if start_type != INTNUM:
            self.report_error(f"Range start must be of type '{INTNUM}', got '{start_type}'.", node.line)
        if end_type != INTNUM:
            self.report_error(f"Range end must be of type '{INTNUM}', got '{end_type}'.", node.line)

        return RANGE

    def visit_MatrixFunction(self, node):

        param_values = [param.value if isinstance(param, AST.IntNum) else self.visit(param) for param in node.params]

        valid_functions = [EYE, ZEROS, ONES]
        if node.name not in valid_functions:
            self.report_error(f"Unknown matrix function '{node.name}'.", node.line)
            return UNKNOWN

        if node.name == EYE:
            if len(param_values) == 1 and (isinstance(param_values[0], int) or param_values[0] == INTNUM) :
                return MATRIX
            else:
                self.report_error(
                    f"{EYE} function requires one integer parameter, got {param_values}.", node.line)
        elif node.name in [ZEROS, ONES]:
            if len(param_values) == 1 and (isinstance(param_values[0], int) or param_values[0] == INTNUM):
                return MATRIX
            elif len(param_values) == 2 and all((isinstance(p, int) or p == INTNUM) for p in param_values):
                return MATRIX
            else:
                self.report_error(
                    f"'{node.name}' function requires one or two integer parameters, got {param_values}.", node.line)

        return UNKNOWN

    def visit_Error(self, node):

        self.report_error(f"{node.message}", node.line)
