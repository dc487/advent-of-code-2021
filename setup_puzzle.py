#!/usr/bin/python3

import pathlib
import sys

if __name__ == "__main__":
    puzzle_name = sys.argv[1]
    pathlib.Path(puzzle_name).mkdir()
    pathlib.Path(puzzle_name + "/input.txt").touch()
    pathlib.Path(puzzle_name + "/" + puzzle_name + ".py").write_text("""import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\\n").splitlines()

if __name__ == "__main__":
    input = load_input()
""")
