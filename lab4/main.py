from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
from lab3.TreePrinter import TreePrinter
from lab4.TypeChecker import TypeChecker
from get_file import get_file

def main() :
    filenames = []
    filenames.append(("control_transfer.m", ["LINE 4: 'continue' statement used outside of a loop.", "LINE 8: 'break' statement used outside of a loop."]))
    filenames.append(("init.m",['Line 3: Matrix rows must have the same size. Found row sizes: [3, 5, 2].']))
    filenames.append(("opers.m",["Line 4: Type mismatch in binary operation '+': 'int' and 'matrix' are not compatible.", "Line 8: Cannot perform operation '+' on matrices of different sizes: [5, 5] and [8, 8].", "Line 13: Type mismatch in binary operation '+': 'vector' and 'matrix' are not compatible.", "Line 17: Cannot perform operation '+' on vectors of different sizes: 5 and 6.", "Line 21: Cannot perform operation '+' on matrices of different sizes: [5, 5] and [5, 7].", 'Line 24: Index 7 out of bounds for dimension 1 of matrix with size [3, 5].', 'Line 24: Index 10 out of bounds for dimension 2 of matrix with size [3, 5].', 'Line 25: Matrix access requires 2 indices, got 3.']))
    print()
    for filename, errors in filenames :

        file = get_file(filename, __file__)
        
        text = file.read()
        lexer = Scanner()
        parser = Mparser()

        ast = parser.parse(lexer.tokenize(text))
        # ast.printTree()
        typeChecker = TypeChecker()
        typeChecker.visit(ast)
        
        print(typeChecker.errors)
        for i in range(max(len(typeChecker.errors), len(errors))) :
            if typeChecker.errors[i] != errors[i] :
                raise Exception("MISMATCHED ERRORS IN", filename)
            print(typeChecker.errors[i])
        print("\n\n======================\n\n")
        
