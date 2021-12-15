import pathlib
from collections import Counter

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

def get_polymer_counts(polymer_pairs, polymer, number_of_steps):
    pairs = []
    for i in range(len(polymer) - 1):
        pairs.append(polymer[i] + polymer[i + 1])

    # Count how many of each pair we expect at the end
    previous_pairs_count = Counter(pairs)
    for i in range(number_of_steps):
        next_pairs_count = Counter()
        for pair in previous_pairs_count.keys():
            next_pairs_count[pair[0] + polymer_pairs[pair]] += previous_pairs_count[pair]
            next_pairs_count[polymer_pairs[pair] + pair[1]] += previous_pairs_count[pair]
        previous_pairs_count = next_pairs_count

    # Use the pair count to count letters
    letter_count = Counter()
    for pair in previous_pairs_count.keys():
        letter_count[pair[0]] += previous_pairs_count[pair]
        letter_count[pair[1]] += previous_pairs_count[pair]

    # First and last letters aren't double counted (yet), so double count them
    letter_count[polymer[0]] += 1
    letter_count[polymer[-1]] += 1

    # Everything is now double counted, so divide by 2 to remove double counting
    for letter in letter_count.keys():
        letter_count[letter] = int(letter_count[letter] / 2)

    return letter_count
    

if __name__ == "__main__":
    input = load_input()

    polymer = input[0]

    polymer_pairs = {}
    for i in range(2, len(input)):
        parts = input[i].split(" -> ")
        polymer_pairs[parts[0]] = parts[1]

    counts = get_polymer_counts(polymer_pairs, polymer, 10).most_common()
    print(counts[0][1] - counts[-1][1])

    counts = get_polymer_counts(polymer_pairs, polymer, 40).most_common()
    print(counts[0][1] - counts[-1][1])
