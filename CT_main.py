
from runner import run
import sys

if __name__ == "__main__":
    run(f"lab5/data/{"fibonacci" if len(sys.argv) == 1 else sys.argv[1]}.m")