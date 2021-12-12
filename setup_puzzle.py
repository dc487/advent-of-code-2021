#!/usr/bin/python3

import pathlib
import sys
from urllib.request import urlopen, Request

if __name__ == "__main__":
    puzzle_day = sys.argv[1]
    puzzle_name = "day_" + puzzle_day.rjust(2, '0') + "_" + sys.argv[2]
    puzzle_path = pathlib.Path(puzzle_name)
    puzzle_path.mkdir()

    with urlopen(Request("https://adventofcode.com/2021/day/" + puzzle_day + "/input", headers = {
        "Cookie": pathlib.Path(".session_cookie").read_text()
    })) as response:
        puzzle_path.joinpath("input.txt").write_bytes(response.read())

    puzzle_path.joinpath(puzzle_name + ".py").write_text("""import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\\n").splitlines()

if __name__ == "__main__":
    input = load_input()
""")

