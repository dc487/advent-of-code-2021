import pathlib
from collections import Counter

def load_input():
    return [int(x) for x in pathlib.Path("./input.txt").read_text().strip("\n").split(",")]

def calculate_total_fish_after_x_days(starting_fish, number_of_days):
    fish_counter = Counter(starting_fish)
    for day in range(number_of_days):
        for fish_index in range(9):
            if fish_index in fish_counter:
                fish_counter[fish_index - 1] = fish_counter[fish_index]
            else:
                fish_counter[fish_index - 1] = 0

        if -1 in fish_counter:
            fish_counter[8] = fish_counter[-1]
            fish_counter[6] += fish_counter[-1]
            fish_counter.pop(-1)

    return sum(fish_counter.values())

if __name__ == "__main__":
    input = load_input()

    print(calculate_total_fish_after_x_days(input, 80))
    print(calculate_total_fish_after_x_days(input, 256))
