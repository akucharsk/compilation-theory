import sys
from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
from get_file import get_file


def main() :

    filenames = []
    filenames.append("example1.m")
    filenames.append("example2.m")
    filenames.append("example3.m")
    filenames.append("additional_test.m")
    print()
    for filename in filenames :

        file = get_file(filename, __file__)
        
        text = file.read()
        lexer = Scanner()
        parser = Mparser(debug = True)

        test = parser.parse(lexer.tokenize(text))
        print(f"File {filename} parsed\n")
        print(test,"\n")
