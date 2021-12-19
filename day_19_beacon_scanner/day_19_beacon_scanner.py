import pathlib
import numpy

class _Scanner:
    def __init__(self, beacon_text):
        lines = beacon_text.splitlines()
        self.beacons = []
        for i in range(1, len(lines)):
            beacon = lines[i]
            parts = beacon.split(",")
            self.beacons.append((int(parts[0]), int(parts[1]), int(parts[2])))
        self.beacons_set = set(self.beacons)

    def get_transformed_beacons(self, rotation, translation):
        rotated_beacons = [numpy.matmul(rotation, x) for x in self.beacons]
        return set([(x[0] + translation[0], x[1] + translation[1], x[2] + translation[2]) for x in rotated_beacons])

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").split("\n\n")

def match_beacons(all_rotations, scanners, scanners_transform_relative_to_scanner0, i):
    for j in range(len(scanners)):
        if i != j and j not in scanners_transform_relative_to_scanner0:
            scanner_i = scanners[i]
            scanner_j = scanners[j]
            for beacon_i in scanner_i.beacons:
                for beacon_j in scanner_j.beacons:
                    for w in range(24):
                        rotation = all_rotations[w]
                        rotated_beacon_j = numpy.matmul(rotation, beacon_j)
                        translation = (beacon_i[0] - rotated_beacon_j[0], beacon_i[1] - rotated_beacon_j[1], beacon_i[2] - rotated_beacon_j[2])

                        transformed_beacons = scanner_j.get_transformed_beacons(rotation, translation)

                        if len([x for x in scanner_i.beacons if x in transformed_beacons]) >= 12:
                            t = scanners_transform_relative_to_scanner0[i]
                            u = numpy.matmul(scanners_transform_relative_to_scanner0[i][3], translation)
                            rot = numpy.matmul(scanners_transform_relative_to_scanner0[i][3], rotation)
                            scanners_transform_relative_to_scanner0[j] = (t[0] + u[0], t[1] + u[1], t[2] + u[2], rot)
                            match_beacons(all_rotations, scanners, scanners_transform_relative_to_scanner0, j)
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break

if __name__ == "__main__":
    input = load_input()

    scanners = [_Scanner(x) for x in input]

    x_rotations = {
        0: [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        1: [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
        2: [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
        3: [[1, 0, 0], [0, 0, 1], [0, -1, 0]]
    }

    all_rotations = {}
    for w in range(24):
        rotation = []
        if (w < 4):
            rotation = x_rotations[w]
        elif (w < 8):
            rotation = numpy.matmul(x_rotations[w % 4], [[-1, 0, 0], [0, 1, 0], [0, 0, -1]])
        elif (w < 12):
            rotation = numpy.matmul(x_rotations[w % 4], [[0, 1, 0], [-1, 0, 0], [0, 0, 1]])
        elif (w < 16):
            rotation = numpy.matmul(x_rotations[w % 4], [[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        elif (w < 20):
            rotation = numpy.matmul(x_rotations[w % 4], [[0, 0, -1], [0, 1, 0], [1, 0, 0]])
        else:
            rotation = numpy.matmul(x_rotations[w % 4], [[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
        all_rotations[w] = rotation

    scanners_transform_relative_to_scanner0 = { 0: (0, 0, 0, all_rotations[0]) }
    match_beacons(all_rotations, scanners, scanners_transform_relative_to_scanner0, 0)

    beacons = set()
    for i in range(len(scanners)):
        transform = scanners_transform_relative_to_scanner0[i]
        rotation = transform[3]
        beacons.update(scanners[i].get_transformed_beacons(rotation, transform))

    print(len(beacons))

    max_manhattan_distance = 0
    for i in range(len(scanners)):
        for j in range(i, len(scanners)):
            if i != j:
                position_i = scanners_transform_relative_to_scanner0[i]
                position_j = scanners_transform_relative_to_scanner0[j]
                manhattan_distance = abs(position_i[0] - position_j[0]) + abs(position_i[1] - position_j[1]) + abs(position_i[2] - position_j[2])
                if manhattan_distance > max_manhattan_distance:
                    max_manhattan_distance = manhattan_distance

    print(max_manhattan_distance)
