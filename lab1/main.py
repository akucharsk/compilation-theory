import sys
import os
from get_file import get_file
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def main() :
    filename = sys.argv[1] if len(sys.argv) > 1 else "example_full.txt"
    file = get_file(filename, __file__)

    text = file.read()
    # print(text)
    lexer = Scanner()
    output = text + "\n\n===\n\n"
    for tok in lexer.tokenize(text):
        # print(tok)
        output += str(tok) + "\n"
        
    result_path = os.path.join(SCRIPT_PATH, 'results', filename.split('.')[0] + "_scanner_result.txt")
    
    try:
        with open(result_path, "w") as result_file:
            result_file.write(output)
    except IOError:
        print(f"Failed to write to the file '{result_path}'.")
        sys.exit(0)
    print(f"Scanning results have been pasted into '{result_path}' ")
    


if __name__ == '__main__':
    from scanner_sly import Scanner
    main()
else :
    from lab1.scanner_sly import Scanner