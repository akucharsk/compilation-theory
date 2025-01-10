import os

from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
from lab3.TreePrinter import TreePrinter
from lab4.TypeChecker import TypeChecker
from get_file import get_file
from itertools import zip_longest
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def main():
    files = os.listdir(os.path.join(SCRIPT_PATH, 'data'))
    files.sort()
    errors = [
        [
            "LINE 4: 'continue' statement used outside of a loop.",
            "LINE 8: 'break' statement used outside of a loop."
        ],

        [
            'LINE 3: Matrix rows must have the same size. Found row sizes: [3, 5, 2].',
            "LINE 14: Variable 'j' is not defined.",
            "LINE 27: Variable 'a' is not defined.",
            "LINE 27: Variable 'b' is not defined.",
            "LINE 30: Variable 'a' is not defined.",
            "LINE 31: Variable 'y' is not defined.",
            "LINE 35: Variable 'i' is not defined.",
            "LINE 36: 'break' statement used outside of a loop."
        ],

        [
            "LINE 4: Type mismatch in binary operation '+': 'int' and 'matrix' are not compatible.",
            "LINE 8: Cannot perform operation '+' on matrices of different sizes: [5, 5] and [8, 8].",
            "LINE 13: Type mismatch in binary operation '+': 'vector' and 'matrix' are not compatible.",
            "LINE 17: Cannot perform operation '+' on vectors of different sizes: 5 and 6.",
            "LINE 21: Cannot perform operation '+' on matrices of different sizes: [5, 5] and [5, 7].",
            'LINE 24: Index 7 out of bounds for dimension 1 of matrix with size [3, 5].',
            'LINE 24: Index 10 out of bounds for dimension 2 of matrix with size [3, 5].',
            'LINE 25: Matrix access requires 2 indices, got 3.',
            'LINE 33: Cannot multiply matrices of shapes [3, 5] and [3, 3].',
            "LINE 35: 'eye' function requires one integer parameter, got [3, 3]."
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
        typeChecker.visit_first(ast)

        # print(typeChecker.errors)
        # for type_checker_error, error in zip_longest(typeChecker.errors, errors):
        #     if type_checker_error != error:
        #         raise Exception("MISMATCHED ERRORS IN " + filename)
        #     print(type_checker_error)
        # print("\n\n======================\n\n")


if __name__ == '__main__':
    main()
