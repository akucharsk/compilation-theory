from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
from lab3.TreePrinter import TreePrinter
from get_file import get_file

def main() :
    filenames = []
    # filenames.append("example1.m")
    # filenames.append("example2.m")
    # filenames.append("example3.m")
    filenames.append("matrix.m")
    print()
    for filename in filenames :

        file = get_file(filename, __file__)
        
        text = file.read()
        lexer = Scanner()
        parser = Mparser(debug = True)

        ast = parser.parse(lexer.tokenize(text))
        
        ast.printTree()

