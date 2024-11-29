from lab3 import AST

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            
            for child in node.instructions:
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
        self.variables = {}

    def report_error(self, message):
        print(f"Error found: {message}")
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
            self.report_error(f"Line {line}: {str(e)}")

    def visit_CompoundStatement(self, node):
        print(f"Visiting CompoundStatement: {node}")
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_BinExpr(self, node):
        print(f"Visiting BinExpr: {node}")
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.op

        if op in ["+", "-", "*", "/"]:
            if not self.compatible(left_type, right_type):
                self.report_error(
                    f"Line {node.line}: Incompatible types {left_type} and {right_type} for operation {op}."
                )

    def visit_RelationExpr(self, node):
        print(f"Visiting RelationExpr: {node}")
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.op

        if not self.compatible(left_type, right_type):
            self.report_error(
                f"Line {node.line}: Incompatible types {left_type} and {right_type} for relational operation {op}."
            )

    def visit_UnaryExpr(self, node):
        print(f"Visiting UnaryExpr: {node}")
        value_type = self.visit(node.value)
        if node.op == "-" and not self.is_numeric(value_type):
            self.report_error(f"Line {node.line}: Unary '-' cannot be applied to non-numeric type {value_type}.")

    def visit_IntNum(self, node):
        print(f"Visiting IntNum: {node}")
        return "int"

    def visit_FloatNum(self, node):
        print(f"Visiting FloatNum: {node}")
        return "float"

    def visit_String(self, node):
        print(f"Visiting String: {node}")
        return "string"

    def visit_Variable(self, node):
        print(f"Visiting Variable: {node}")
        symbol = self.lookup_variable(node.name)
        print(symbol)
        if symbol is None:
            self.report_error(f"Line {node.line}: Undefined variable '{node.name}'.")
            return None
        return symbol.type

    def visit_Assignment(self, node):
        print(f"Visiting Assignment: {node}")
        self.variables[node.id] = node.value.value
        print(self.variables)
        # variable_type = self.visit(node.id)
        # value_type = self.visit(node.value)
        # if not self.compatible(variable_type, value_type):
        #     self.report_error(
        #         f"Line {node.line}: Cannot assign value of type {value_type} to variable of type {variable_type}."
        #     )

    def visit_ConditionalInstruction(self, node):
        print(f"Visiting ConditionalInstruction: {node}")
        condition_type = self.visit(node.condition)
        if condition_type != "bool":
            self.report_error(f"Line {node.line}: Condition must evaluate to 'bool', not {condition_type}.")
        self.visit(node.instructions)
        if node.else_instruction:
            self.visit(node.else_instruction)

    def visit_WhileLoop(self, node):
        print(f"Visiting WhileLoop: {node}")
        condition_type = self.visit(node.condition)
        if condition_type != "bool":
            self.report_error(f"Line {node.line}: Condition must evaluate to 'bool', not {condition_type}.")
        self.in_loop += 1
        self.visit(node.instructions)
        self.in_loop -= 1

    def visit_ForLoop(self, node):
        print(f"Visiting ForLoop: {node}")
        range_type = self.visit(node.range)
        if range_type != "range":
            self.report_error(f"Line {node.line}: Loop range must evaluate to 'range', not {range_type}.")
        self.in_loop += 1
        self.visit(node.instructions)
        self.in_loop -= 1

    def visit_Break(self, node):
        print(f"Visiting Break: {node}")
        if self.in_loop <= 0:
            self.report_error(f"Line {node.line}: 'break' used outside of a loop.")

    def visit_ContinueInstruction(self, node):
        print(f"Visiting Continue: {node}")
        if self.in_loop <= 0 :
            self.report_error(f"Line {node.line}: 'continue' used outside of a loop.")

    def visit_ReturnInstruction(self, node):
        print(f"Visiting ReturnInstruction: {node}")
        value_type = self.visit(node.value)

    def visit_PrintInstruction(self, node):
        print(f"Visiting PrintInstruction: {node}")
        self.visit(node.value)

    def visit_MatrixFunction(self, node):
        print(f"Visiting MatrixFunction: {node}")
        if node.name in ["eye", "zeros", "ones"]:
            for param in node.params:
                param_type = self.visit(param)
                if param_type != "int":
                    self.report_error(f"Line {node.line}: Parameters for {node.name} must be integers.")

    def visit_Matrix(self, node):
        print(f"Visiting Matrix: {node}")
        row_lengths = [len(row) for row in node.rows]
        if len(set(row_lengths)) > 1:
            self.report_error(f"Line {node.line}: Rows of matrix have inconsistent lengths.")
        for row in node.rows:
            for element in row:
                self.visit(element)

    def visit_MatrixAccess(self, node):
        print(f"Visiting MatrixAccess: {node}")
        matrix_type = self.visit(node.matrix)
        row_index = self.visit(node.row)
        col_index = self.visit(node.col)

        if isinstance(row_index, int) and isinstance(col_index, int):
            rows, cols = matrix_type.shape
            if row_index < 0 or row_index >= rows or col_index < 0 or col_index >= cols:
                self.report_error(f"Line {node.line}: Matrix access out of bounds.")

    def visit_Vector(self, node):
        print(f"Visiting Vector: {node}")
        for element in node.elements:
            self.visit(element)

    def visit_ArrayAccess(self, node):
        print(f"Visiting ArrayAccess: {node}")
        array_type = self.visit(node.id)
        if not isinstance(array_type, list):
            self.report_error(f"Line {node.line}: Cannot index non-array type {array_type}.")
        for index in node.indices:
            index_type = self.visit(index)
            if index_type != "int":
                self.report_error(f"Line {node.line}: Array index must be of type 'int', not {index_type}.")

    def visit_Error(self, node):
        print(f"Visiting Error: {node}")
        self.report_error(f"Line {node.line}: {node.message}")

    def compatible(self, type1, type2):
        print(f"Checking compatibility: {type1} and {type2}")
        return type1 == type2

    def is_numeric(self, type_):
        print(f"Checking if type is numeric: {type_}")
        return type_ in ["int", "float"]

    def lookup_variable(self, name):
        print(f"Looking up variable: {name}")
        print(self.variables)
        print(self.variables.get(name, None))
        
        return self.variables.get(name, None)
