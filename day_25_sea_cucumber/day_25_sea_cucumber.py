import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

def move_cucumbers(current_state):
    cucumbers_moved = 0

    east_state = [x[:] for x in current_state]
    for y, line in enumerate(current_state):
        for x, character in enumerate(line):
            if character == ">" and line[(x + 1) % len(line)] == ".":
                if (x + 1 < len(line)):
                    east_state[y] = east_state[y][:x] + ".>" + east_state[y][x+2:]
                else:
                    east_state[y] = ">" + east_state[y][1:len(line) - 1] + "."
                cucumbers_moved += 1

    north_state = [x[:] for x in east_state]
    for y, line in enumerate(east_state):
        for x, character in enumerate(line):
            if character == "v" and east_state[(y + 1) % len(east_state)][x] == ".":
                north_state[y] = north_state[y][:x] + "." + north_state[y][x+1:]
                north_state[(y + 1) % len(east_state)] = north_state[(y + 1) % len(east_state)][:x] + "v" + north_state[(y + 1) % len(east_state)][x+1:]
                cucumbers_moved += 1

    return (north_state, cucumbers_moved)

    

if __name__ == "__main__":
    input = load_input()

    next_state, cucumbers_moved = move_cucumbers(input)

    step = 1
    while cucumbers_moved != 0:
        step += 1
        next_state, cucumbers_moved = move_cucumbers(next_state)

    print(step)
    
