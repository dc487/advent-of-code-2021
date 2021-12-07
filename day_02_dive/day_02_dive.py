import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

if __name__ == "__main__":
    input = load_input()

    horizontal = 0
    depth = 0
    for command in input:
        command_parts = command.split(" ")
        direction = command_parts[0]
        number = int(command_parts[1])
        if direction == "forward":
            horizontal += number
        elif direction == "down":
            depth += number
        elif direction == "up":
            depth -= number

    print(horizontal, depth, horizontal * depth)

    horizontal = 0
    depth = 0
    aim = 0
    for command in input:
        command_parts = command.split(" ")
        direction = command_parts[0]
        number = int(command_parts[1])
        if direction == "forward":
            horizontal += number
            depth += aim * number
        elif direction == "down":
            aim += number
        elif direction == "up":
            aim -= number
            
    print(horizontal, depth, horizontal * depth)
