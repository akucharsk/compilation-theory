import sys
# import ply.yacc as yacc
from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
from lab3.TreePrinter import TreePrinter
from lab4.TypeChecker import TypeChecker
from lab5.Interpreter import Interpreter
from get_file import get_file


def main():
    filenames = ["fibonacci.m", "matrix.m", "pi.m", "primes.m", "sqrt.m", "triangle.m"]
    # filenames = ["matrix.m"]
    
    for filename in filenames:
        try:
            # filename = sys.argv[1] if len(sys.argv) > 1 else "fibonacci.m"
            file = get_file(filename, __file__)
        except IOError:
            print("Cannot open {0} file".format(filename))
            sys.exit(0)

        parser = Mparser()
        lexer = Scanner()
        # parser = yacc.yacc(module=Mparser)
        text = file.read()

        ast = parser.parse(lexer.tokenize(text))

        # Below code shows how to use visitor
        typeChecker = TypeChecker()
        typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
        # if not typeChecker.correct : continue
        interpreter = Interpreter()
        interpreter.visit(ast)

        print('---{=======}---\n')
        
    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())


if __name__ == '__main__':
    main()
    