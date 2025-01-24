import sys
# import ply.yacc as yacc
from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
from lab4.TypeChecker import TypeChecker
from lab5.Interpreter import Interpreter
from get_file import get_file
from printing import print_color


def main():
    filenames = []
    filenames.append("fibonacci.m")
    # filenames.append("matrix.m")
    # filenames.append("pi.m")
    # filenames.append("primes.m")
    # filenames.append("sqrt.m")
    # filenames.append("triangle.m")
    
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
        
        # if len(ast) == 0 : continue
        try :
            ast[0]
            continue
        except :
            pass
        
        # ast.printTree()

        # Below code shows how to use visitor
        typeChecker = TypeChecker()
        typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
        if not typeChecker.correct : 
            print("Errors found")
            continue
        
        try :
            interpreter = Interpreter()
            interpreter.visit(ast)
        except KeyboardInterrupt :
            print_color("\nProgram killed by user")
            continue
        except Exception as e :
            print_color(e)
            continue
        
        print('---{=======}---\n')
        
    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())

if __name__ == '__main__':
    main()
    