import pathlib

def load_input():
    return [int(x) for x in pathlib.Path("./input.txt").read_text().strip("\n").splitlines()]

if __name__ == "__main__":
    input = load_input()

    increase_count = 0
    for index in range(len(input) - 1):
        if (input[index] < input[index + 1]):
            increase_count += 1
    
    print(increase_count)

    increase_count = 0
    for index in range(len(input) - 3):
        first_total = input[index] + input[index + 1] + input[index + 2]
        second_total = input[index + 1] + input[index + 2] + input[index + 3]
        if (first_total < second_total):
            increase_count += 1

    print(increase_count)
