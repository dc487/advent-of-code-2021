import pathlib

class _RebootStep:
    def __init__(self, instruction):
        parts = instruction.split(" ")
        self.action = parts[0]
        self.is_on_action = self.action == "on"
        coordinates = parts[1].split(",")
        xParts = coordinates[0].replace("x=", "").split("..")
        self.x_from = int(xParts[0])
        self.x_to = int(xParts[1])
        yParts = coordinates[1].replace("y=", "").split("..")
        self.y_from = int(yParts[0])
        self.y_to = int(yParts[1])
        zParts = coordinates[2].replace("z=", "").split("..")
        self.z_from = int(zParts[0])
        self.z_to = int(zParts[1])

class _Region:
    def __init__(self, x_from, x_to, y_from, y_to, z_from, z_to):
        self.x_from = x_from
        self.x_to = x_to
        self.y_from = y_from
        self.y_to = y_to
        self.z_from = z_from
        self.z_to = z_to
    
    def size(self):
        if (self.x_to < self.x_from or self.y_to < self.y_from or self.z_to < self.z_from):
            return 0

        return (self.x_to - self.x_from + 1) * (self.y_to - self.y_from + 1) * (self.z_to - self.z_from + 1)

    def collides_with(self, other):
        collides_x = self.x_from <= other.x_to and self.x_to >= other.x_from
        collides_y = self.y_from <= other.y_to and self.y_to >= other.y_from
        collides_z = self.z_from <= other.z_to and self.z_to >= other.z_from
        return collides_x and collides_y and collides_z

    def minus(self, other):
        surviving_parts = []
        surviving_parts.append(_Region(self.x_from, other.x_from - 1, self.y_from, other.y_from - 1, self.z_from, other.z_from - 1))
        surviving_parts.append(_Region(max(self.x_from, other.x_from), min(self.x_to, other.x_to), self.y_from, other.y_from - 1, self.z_from, other.z_from - 1))
        surviving_parts.append(_Region(other.x_to + 1, self.x_to, self.y_from, other.y_from - 1, self.z_from, other.z_from - 1))

        surviving_parts.append(_Region(self.x_from, other.x_from - 1, max(self.y_from, other.y_from), min(self.y_to, other.y_to), self.z_from, other.z_from - 1))
        surviving_parts.append(_Region(max(self.x_from, other.x_from), min(self.x_to, other.x_to), max(self.y_from, other.y_from), min(self.y_to, other.y_to), self.z_from, other.z_from - 1))
        surviving_parts.append(_Region(other.x_to + 1, self.x_to, max(self.y_from, other.y_from), min(self.y_to, other.y_to), self.z_from, other.z_from - 1))

        surviving_parts.append(_Region(self.x_from, other.x_from - 1, other.y_to + 1, self.y_to, self.z_from, other.z_from - 1))
        surviving_parts.append(_Region(max(self.x_from, other.x_from), min(self.x_to, other.x_to), other.y_to + 1, self.y_to, self.z_from, other.z_from - 1))
        surviving_parts.append(_Region(other.x_to + 1, self.x_to, other.y_to + 1, self.y_to, self.z_from, other.z_from - 1))
        

        surviving_parts.append(_Region(self.x_from, other.x_from - 1, self.y_from, other.y_from - 1, max(self.z_from, other.z_from), min(self.z_to, other.z_to)))
        surviving_parts.append(_Region(max(self.x_from, other.x_from), min(self.x_to, other.x_to), self.y_from, other.y_from - 1, max(self.z_from, other.z_from), min(self.z_to, other.z_to)))
        surviving_parts.append(_Region(other.x_to + 1, self.x_to, self.y_from, other.y_from - 1, max(self.z_from, other.z_from), min(self.z_to, other.z_to)))

        surviving_parts.append(_Region(self.x_from, other.x_from - 1, max(self.y_from, other.y_from), min(self.y_to, other.y_to), max(self.z_from, other.z_from), min(self.z_to, other.z_to)))
        surviving_parts.append(_Region(other.x_to + 1, self.x_to, max(self.y_from, other.y_from), min(self.y_to, other.y_to), max(self.z_from, other.z_from), min(self.z_to, other.z_to)))

        surviving_parts.append(_Region(self.x_from, other.x_from - 1, other.y_to + 1, self.y_to, max(self.z_from, other.z_from), min(self.z_to, other.z_to)))
        surviving_parts.append(_Region(max(self.x_from, other.x_from), min(self.x_to, other.x_to), other.y_to + 1, self.y_to, max(self.z_from, other.z_from), min(self.z_to, other.z_to)))
        surviving_parts.append(_Region(other.x_to + 1, self.x_to, other.y_to + 1, self.y_to, max(self.z_from, other.z_from), min(self.z_to, other.z_to)))

        
        surviving_parts.append(_Region(self.x_from, other.x_from - 1, self.y_from, other.y_from - 1, other.z_to + 1, self.z_to))
        surviving_parts.append(_Region(max(self.x_from, other.x_from), min(self.x_to, other.x_to), self.y_from, other.y_from - 1, other.z_to + 1, self.z_to))
        surviving_parts.append(_Region(other.x_to + 1, self.x_to, self.y_from, other.y_from - 1, other.z_to + 1, self.z_to))

        surviving_parts.append(_Region(self.x_from, other.x_from - 1, max(self.y_from, other.y_from), min(self.y_to, other.y_to), other.z_to + 1, self.z_to))
        surviving_parts.append(_Region(max(self.x_from, other.x_from), min(self.x_to, other.x_to), max(self.y_from, other.y_from), min(self.y_to, other.y_to), other.z_to + 1, self.z_to))
        surviving_parts.append(_Region(other.x_to + 1, self.x_to, max(self.y_from, other.y_from), min(self.y_to, other.y_to), other.z_to + 1, self.z_to))

        surviving_parts.append(_Region(self.x_from, other.x_from - 1, other.y_to + 1, self.y_to, other.z_to + 1, self.z_to))
        surviving_parts.append(_Region(max(self.x_from, other.x_from), min(self.x_to, other.x_to), other.y_to + 1, self.y_to, other.z_to + 1, self.z_to))
        surviving_parts.append(_Region(other.x_to + 1, self.x_to, other.y_to + 1, self.y_to, other.z_to + 1, self.z_to))

        return [x for x in surviving_parts if x.size() > 0]

    def print(self):
        print("new region:")
        for x in range(self.x_from, self.x_to + 1):
            for y in range(self.y_from, self.y_to + 1):
                for z in range(self.z_from, self.z_to + 1):
                    print(x, y, z)
                    
def load_input():
    return [_RebootStep(x) for x in pathlib.Path("./input.txt").read_text().strip("\n").splitlines()]

if __name__ == "__main__":
    input = load_input()

    cubes = []
    for x in range(-50, 51):
        x_array = []
        for y in range(-50, 51):
            y_array = []
            for z in range(-50, 51):
                y_array.append(False)
            x_array.append(y_array)
        cubes.append(x_array)


    on_cubes = set()
    for step in input:
        x_from = min(50, max(-50, step.x_from)) + 50
        x_to = min(50, max(-50, step.x_to)) + 50
        if x_from == x_to:
            continue

        y_from = min(50, max(-50, step.y_from)) + 50
        y_to = min(50, max(-50, step.y_to)) + 50
        if y_from == y_to:
            continue

        z_from = min(50, max(-50, step.z_from)) + 50
        z_to = min(50, max(-50, step.z_to)) + 50
        if z_from == z_to:
            continue

        for x in range(x_from, x_to + 1):
            for y in range(y_from, y_to + 1):
                for z in range(z_from, z_to + 1):
                    if step.is_on_action:
                        cubes[x][y][z] = True
                    else:
                        cubes[x][y][z] = False

    total_on_cubes = 0
    for x_array in cubes:
        for y_array in x_array:
            total_on_cubes += len([z for z in y_array if z])
    print(total_on_cubes)

    on_regions = []
    for step in input:
        next_on_regions = []
        current_region = _Region(step.x_from, step.x_to, step.y_from, step.y_to, step.z_from, step.z_to)
        for on_region in on_regions:
            if current_region.collides_with(on_region):
                # Chop the on_region into parts and add all of them except the one that overlaps
                # If it's an "on" instruction, this overlapping part will be turned on again when we add this region
                # If it's an "off" instruction, this effectively turns the overlapping part off
                next_on_regions += on_region.minus(current_region)
            else:
                next_on_regions.append(on_region)

        if step.is_on_action:
            next_on_regions.append(current_region)

        on_regions = next_on_regions

    print(sum([x.size() for x in on_regions]))

