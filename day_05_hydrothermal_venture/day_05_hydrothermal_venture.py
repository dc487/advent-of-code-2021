import pathlib
from collections import Counter

class _Point:
    def __init__(self, point_definition):
        point_parts = point_definition.split(",")
        self.point = point_definition
        self.x = int(point_parts[0])
        self.y = int(point_parts[1])

class _Line:
    def __init__(self, line_definition):
        line_parts = line_definition.split(" -> ")
        self.line = line_definition
        self.point_from = _Point(line_parts[0])
        self.point_to = _Point(line_parts[1])


def load_input():
    return [_Line(x) for x in pathlib.Path("./input.txt").read_text().strip("\n").splitlines()]

if __name__ == "__main__":
    input = load_input()

    horizontal_lines = [l for l in input if l.point_from.y == l.point_to.y]
    vertical_lines = [l for l in input if l.point_from.x == l.point_to.x]

    visited_points = []
    for line in horizontal_lines:
        x1 = min(line.point_from.x, line.point_to.x)
        x2 = max(line.point_from.x, line.point_to.x)

        for x in range(x1, x2 + 1):
            visited_points.append(str(x) + "," + str(line.point_from.y))

    for line in vertical_lines:
        y1 = min(line.point_from.y, line.point_to.y)
        y2 = max(line.point_from.y, line.point_to.y)

        for y in range(y1, y2 + 1):
            visited_points.append(str(line.point_from.x) + "," + str(y))

    counts = Counter(visited_points)
    print(len([x for x in counts.values() if x > 1]))

    other_lines = [l for l in input if l.point_from.y != l.point_to.y and l.point_from.x != l.point_to.x]
    for line in other_lines:
        x1 = line.point_from.x
        x2 = line.point_to.x

        y1 = line.point_from.y
        y2 = line.point_to.y

        if (x1 < x2):
            for x in range(x1, x2 + 1):
                y = 0
                if (y1 < y2):
                    y = y1 + x - x1
                else:
                    y = y1 - x + x1

                visited_points.append(str(x) + "," + str(y))
        else:
            for x in range(x2, x1 + 1):
                y = 0
                if (y2 < y1):
                    y = y2 + x - x2
                else:
                    y = y2 - x + x2

                visited_points.append(str(x) + "," + str(y))

    counts = Counter(visited_points)
    print(len([x for x in counts.values() if x > 1]))