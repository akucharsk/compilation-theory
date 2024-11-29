from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
from lab3.TreePrinter import TreePrinter
from lab4.TypeChecker import TypeChecker
from get_file import get_file

def main() :
    filenames = []
    filenames.append("control_transfer.m")
    filenames.append("init.m")
    filenames.append("opers.m")
    print()
    for filename in filenames :

        file = get_file(filename, __file__)
        
        text = file.read()
        lexer = Scanner()
        parser = Mparser()

        ast = parser.parse(lexer.tokenize(text))
        ast.printTree()
        typeChecker = TypeChecker()
        typeChecker.visit(ast)
