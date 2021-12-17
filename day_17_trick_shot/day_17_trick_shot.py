import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

def get_max_y(target_x_1, target_y_1, target_x_2, target_y_2, initial_x_velocity, intitial_y_velocity):
    max_y = 0
    x = 0
    y = 0
    x_velocity = initial_x_velocity
    y_velocity = intitial_y_velocity

    while x <= target_x_2 and y >= min(target_y_1, target_y_2):
        x += x_velocity
        y += y_velocity

        if (y > max_y):
            max_y = y

        if (target_x_1 <= x and target_x_2 >= x and target_y_1 <= y and target_y_2 >= y):
            return max_y

        if (x_velocity > 0):
            x_velocity -= 1
        elif (x_velocity < 0):
            x_velocity += 1
        y_velocity -= 1

    return -1

if __name__ == "__main__":
    input = load_input()

    parts = input[0].replace("target area: ", "").split(", ")
    x_parts = parts[0].replace("x=", "").split("..")
    target_x_1 = int(x_parts[0])
    target_x_2 = int(x_parts[1])
    y_parts = parts[1].replace("y=", "").split("..")
    target_y_1 = int(y_parts[0])
    target_y_2 = int(y_parts[1])

    max_y_positions = []
    for x in range(target_x_2):
        for y in range(100):
            max_y_positions.append(get_max_y(target_x_1, target_y_1, target_x_2, target_y_2, x, y))

    print(max(max_y_positions))

    total_valid_velocities = 0
    for x in range(target_x_2 + 1):
        for y in range(-100, 100):
            if get_max_y(target_x_1, target_y_1, target_x_2, target_y_2, x, y) >= 0:
                total_valid_velocities += 1

    print(total_valid_velocities)
