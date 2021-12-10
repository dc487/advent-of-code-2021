import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

def flood_fill(filled_nodes, height_map, x, y):
    if (height_map[x][y] == 9):
        return

    point = str(x) + "," + str(y)
    if point not in filled_nodes:
        filled_nodes.add(point)
        flood_fill(filled_nodes, height_map, x, y-1)
        flood_fill(filled_nodes, height_map, x, y+1)
        flood_fill(filled_nodes, height_map, x+1, y)
        flood_fill(filled_nodes, height_map, x-1, y)

if __name__ == "__main__":
    input = load_input()

    nines = [9] * (len(input[0]) + 2)
    height_map = [nines] + [[9] + [int(y) for y in x] + [9] for x in input] + [nines]

    low_points = []
    basins = []
    for x in range(1, len(input[0]) + 1):
        for y in range(1, len(input) + 1):
            point = height_map[x][y]
            if (point < height_map[x-1][y] and point < height_map[x+1][y] and point < height_map[x][y-1] and point < height_map[x][y+1]):
                low_points.append(point)
                basin = set()
                flood_fill(basin, height_map, x, y)
                basins.append(basin)

    print(sum([x + 1 for x in low_points]))
    largest_basin_sizes = sorted([len(x) for x in basins])[-3::]
    print(largest_basin_sizes[0] * largest_basin_sizes[1] * largest_basin_sizes[2])

