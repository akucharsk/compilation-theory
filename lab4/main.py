import os

from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
from lab3.TreePrinter import TreePrinter
from lab4.TypeChecker import TypeChecker
from get_file import get_file
from itertools import zip_longest


def main():
    files = os.listdir('data')
    files.sort()
    errors = [
        [
            "LINE 4: 'continue' statement used outside of a loop.",
            "LINE 8: 'break' statement used outside of a loop."
        ],

        [
            'Line 3: Matrix rows must have the same size. Found row sizes: [3, 5, 2].',
            "Line 14: Variable 'j' is not defined.",
            "Line 27: Variable 'a' is not defined.",
            "Line 27: Variable 'b' is not defined.",
            "Line 30: Variable 'a' is not defined.",
            "Line 31: Variable 'y' is not defined.",
            "Line 35: Variable 'i' is not defined.",
            "LINE 36: 'break' statement used outside of a loop."
        ],

        [
            "Line 4: Type mismatch in binary operation '+': 'int' and 'matrix' are not compatible.",
            "Line 8: Cannot perform operation '+' on matrices of different sizes: [5, 5] and [8, 8].",
            "Line 13: Type mismatch in binary operation '+': 'vector' and 'matrix' are not compatible.",
            "Line 17: Cannot perform operation '+' on vectors of different sizes: 5 and 6.",
            "Line 21: Cannot perform operation '+' on matrices of different sizes: [5, 5] and [5, 7].",
            'Line 24: Index 7 out of bounds for dimension 1 of matrix with size [3, 5].',
            'Line 24: Index 10 out of bounds for dimension 2 of matrix with size [3, 5].',
            'Line 25: Matrix access requires 2 indices, got 3.'
        ]
    ]

    filenames = {file: error for file, error in zip_longest(files, errors)}
    print()
    for filename, errors in filenames.items():

        file = get_file(filename, __file__)

        text = file.read()
        lexer = Scanner()
        parser = Mparser()

        ast = parser.parse(lexer.tokenize(text))
        # ast.printTree()
        typeChecker = TypeChecker()
        typeChecker.visit(ast)

        print(typeChecker.errors)
        for type_checker_error, error in zip_longest(typeChecker.errors, errors):
            if type_checker_error != error:
                raise Exception("MISMATCHED ERRORS IN " + filename)
            print(type_checker_error)
        print("\n\n======================\n\n")


if __name__ == '__main__':
    main()
