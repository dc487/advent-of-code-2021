import pathlib

def load_input():
    return [int(x) for x in pathlib.Path("./input.txt").read_text().strip("\n").split(",")]

if __name__ == "__main__":
    input = load_input()

    fuel_amounts = [sum([abs(i - x) for x in input]) for i in range(2000)]
    fuel_amounts.sort()

    total_fuel = fuel_amounts[0]

    print(total_fuel)

    fuel_amounts = [sum([abs(i - x) * (abs(i - x) + 1) / 2 for x in input]) for i in range(2000)]
    fuel_amounts.sort()

    total_fuel = fuel_amounts[0]

    print(total_fuel)
