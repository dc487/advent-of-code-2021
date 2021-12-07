import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

if __name__ == "__main__":
    input = load_input()

    gamma_string = ""
    epsilon_string = ""
    for index in range(len(input[0])):
        if (sum([int(x[index]) for x in input]) > len(input) / 2):
            gamma_string += "1"
            epsilon_string += "0"
        else:
            gamma_string += "0"
            epsilon_string += "1"

    gamma = int(gamma_string, 2)
    epsilon = int(epsilon_string, 2)

    print(gamma, epsilon, gamma * epsilon)

    for index in range(len(input[0])):
        if (sum([int(x[index]) for x in input]) >= len(input) / 2):
            input = [x for x in input if x[index] == "1"]
        else:
            input = [x for x in input if x[index] == "0"]

        if (len(input) == 1):
            oxygen_generator_rating = int(input[0], 2)
            break

    input = load_input()
    for index in range(len(input[0])):
        if (sum([int(x[index]) for x in input]) >= len(input) / 2):
            input = [x for x in input if x[index] == "0"]
        else:
            input = [x for x in input if x[index] == "1"]

        if (len(input) == 1):
            co2_scrubber_rating = int(input[0], 2)
            break

    print(oxygen_generator_rating, co2_scrubber_rating, oxygen_generator_rating * co2_scrubber_rating)


