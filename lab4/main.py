import os

from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
from lab4.TypeChecker import TypeChecker
from get_file import get_file
from itertools import zip_longest

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def main():
    filenames = os.listdir(os.path.join(SCRIPT_PATH, 'data'))
    filenames.sort()

    filenames = ['matrix.m']
    
    for filename in filenames:

        file = get_file(filename, __file__)

        text = file.read()
        lexer = Scanner()
        parser = Mparser()

        ast = parser.parse(lexer.tokenize(text))
        print(ast)
        ast.printTree()
        print()
        typeChecker = TypeChecker()
        typeChecker.visit_first(ast)


if __name__ == '__main__':
    main()
