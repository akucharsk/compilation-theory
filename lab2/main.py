import sys
from lab1.scanner_sly import Scanner
from lab2.parser_sly import Mparser
import os
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


def get_file(filename) :
    try:
        # filename = sys.argv[1] if len(sys.argv) > 1 else (input("Enter filename: ") or "example3.m")
        print("File chosen:", filename)
        file = open(os.path.join(SCRIPT_PATH, "data", filename), "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)
    return file


def main() :

    filenames = []
    filenames.append("example1.m")
    filenames.append("example2.m")
    filenames.append("example3.m")
    filenames.append("additional_test.m")
    print()
    for filename in filenames :

        file = get_file(filename)
        
        text = file.read()
        lexer = Scanner()
        parser = Mparser()

        test = parser.parse(lexer.tokenize(text))
        print(f"File {filename} parsed\n")
        print(test,"\n")
