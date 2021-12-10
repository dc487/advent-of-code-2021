import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

if __name__ == "__main__":
    input = load_input()

    total = 0
    bracket_pairs = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">"
    }
    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }

    for line in input:
        stack = []
        for character in line:
            if (character in bracket_pairs.keys()):
                stack.append(bracket_pairs[character])
            else:
                expected_character = stack.pop()
                if (expected_character != character):
                    total += scores[character]
                    break

    print(total)

    point_values = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }

    scores = []
    for line in input:
        total = 0
        stack = []
        for character in line:
            if (character in bracket_pairs.keys()):
                stack.append(bracket_pairs[character])
            else:
                expected_character = stack.pop()
                if (expected_character != character):
                    break
        else:
            for char in reversed(stack):
                total *= 5
                total += point_values[char]
            scores.append(total)

    print(scores)
    scores.sort()
    mid_point = len(scores) / 2
    if (mid_point % 2 == 1):
        mid_point -= 0.5
    print(scores[int(mid_point)])


