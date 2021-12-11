import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

def add_one_if_in_range(grid, x, y):
    width = len(grid[0])
    height = len(grid)

    if (x-1 >= 0):
        if (y-1 >= 0):
            grid[x-1][y-1] += 1
        grid[x-1][y] += 1
        if (y+1 < height):
            grid[x-1][y+1] += 1

    if (y-1 >= 0):
        grid[x][y-1] += 1
    if (y+1 < height):
        grid[x][y+1] += 1
    
    if (x+1 < width):
        if (y-1 >= 0):
            grid[x+1][y-1] += 1
        grid[x+1][y] += 1
        if (y+1 < height):
            grid[x+1][y+1] += 1



def recursive_flash(flashes, grid, x, y):
    width = len(grid[0])
    height = len(grid)

    if (x < 0 or x >= width or y < 0 or y>= height):
        return

    if (grid[x][y] <= 9):
        return

    point = str(x) + "," + str(y)
    if point not in flashes:
        flashes.add(point)
        add_one_if_in_range(grid, x, y)
        grid[x][y] += 1
        grid[x][y] += 1
        grid[x][y] += 1
        grid[x][y] += 1
        grid[x][y] += 1
        recursive_flash(flashes, grid, x-1, y-1)
        recursive_flash(flashes, grid, x, y-1)
        recursive_flash(flashes, grid, x+1, y-1)
        recursive_flash(flashes, grid, x-1, y)
        recursive_flash(flashes, grid, x+1, y)
        recursive_flash(flashes, grid, x-1, y+1)
        recursive_flash(flashes, grid, x, y+1)
        recursive_flash(flashes, grid, x+1, y+1)

def perform_step(grid):
    width = len(grid[0])
    height = len(grid)

    for x in range(width):
        for y in range(height):
            grid[x][y] += 1

    flashes = set()
    for x in range(width):
        for y in range(height):
            recursive_flash(flashes, grid, x, y)

    for x in range(width):
        for y in range(height):
            if grid[x][y] > 9:
                grid[x][y] = 0

    return flashes

if __name__ == "__main__":
    input = load_input()

    grid = [[int(y) for y in x] for x in input]
    
    total = 0
    for i in range(100):
        flashes = perform_step(grid)
        total += len(flashes)

    print(total)

    grid = [[int(y) for y in x] for x in input]
    width = len(grid[0])
    height = len(grid)
    synchronised_flash_total = width*height
    step = 0
    while(True):
        step += 1
        flashes = perform_step(grid)
        if len(flashes) == synchronised_flash_total:
            print(step)
            break
