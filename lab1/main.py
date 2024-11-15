import sys
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def main() :
    filename = sys.argv[1] if len(sys.argv) > 1 else "example_full.txt"
    try:
        file = open(os.path.join(SCRIPT_PATH, 'data', filename), "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    # print(text)
    lexer = Scanner()
    line = 1
    # print(float('62.51E2'))
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
    print(f"data have been pasted into '{result_path}' ")
    


if __name__ == '__main__':
    from scanner_sly import Scanner
    main()
else :
    from lab1.scanner_sly import Scanner