import sys
from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
from lab4.TypeChecker import TypeChecker
from lab5.Interpreter import Interpreter
from printing import print_color


def run(filename) :
    
    try:
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser()
    lexer = Scanner()
    text = file.read()

    ast = parser.parse(lexer.tokenize(text))
    
    if hasattr(ast, '__iter__') or hasattr(ast, '__getitem__'):
        return
    

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
    if not typeChecker.correct :
        return
    
    try :
        interpreter = Interpreter()
        return interpreter.visit(ast)
    except KeyboardInterrupt :
        print_color("\nProgram killed by user")
        return
    except Exception as e :
        print_color(e)
    return
    