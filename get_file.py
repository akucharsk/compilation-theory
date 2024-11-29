import os
import sys

def get_file(filename, origin) :
    SCRIPT_PATH = os.path.dirname(os.path.realpath(origin))
    
    try:
        # filename = sys.argv[1] if len(sys.argv) > 1 else (input("Enter filename: ") or "example3.m")
        print("File chosen:", filename)
        file = open(os.path.join(SCRIPT_PATH, "data", filename), "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)
    return file