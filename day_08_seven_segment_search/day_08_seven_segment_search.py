import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

if __name__ == "__main__":
    input = load_input()

    count = 0
    for line in input:
        parts = [x for x in line.split(" | ")[1].split(" ") if len(x) in {2, 4, 3, 7}]
        count += len(parts)

    print(count)

    number_patterns = {
        'abcefg': '0',
        'cf': '1',
        'acdeg': '2',
        'acdfg': '3',
        'bcdf': '4',
        'abdfg': '5',
        'abdefg': '6',
        'acf': '7',
        'abcdefg': '8',
        'abcdfg': '9',
    }

    total = 0
    for line in input:
        parts = line.split(" | ")
        lookup = {}
        numbers = parts[0].split(" ")
        zero = ""
        [one] = (x for x in numbers if len(x) == 2)
        two = ""
        three = ""
        [four] = (x for x in numbers if len(x) == 4)
        five = ""
        six = ""
        [seven] = (x for x in numbers if len(x) == 3)
        [eight] = (x for x in numbers if len(x) == 7)
        nine = ""

        c = ""
        e = ""

        for digit in seven:
            if digit not in one:
                lookup[digit] = 'a'

        length_six_numbers = [x for x in numbers if len(x) == 6]
        for n in length_six_numbers:
            for digit in seven:
                if digit not in n:
                    six = n
                    lookup[digit] = 'c'
                    c = digit
                    length_six_numbers = [x for x in length_six_numbers if x !=  six]

        for digit in one:
            if digit != c:
                lookup[digit] = 'f'

        length_five_numbers = [x for x in numbers if len(x) == 5]
        for n in length_five_numbers:
            for digit in n:
                if digit not in six:
                    break
            else:
                five = n
                length_five_numbers = [x for x in length_five_numbers if x != five]

        for digit in six:
            if digit not in five:
                lookup[digit] = 'e'
                e = digit
                break

        for n in length_five_numbers:
            if e in n:
                two = n
            else:
                three = n

        for digit in four:
            if digit not in three:
                lookup[digit] = 'b'
                break

        for n in length_six_numbers:
            if e in n:
                zero = n
            else:
                nine = n

        for digit in four:
            if digit not in zero:
                lookup[digit] = 'd'

        for digit in zero:
            if digit not in lookup.keys():
                lookup[digit] = 'g'
                break

        output = int(''.join([number_patterns[''.join(sorted([lookup[y] for y in x]))] for x in parts[1].split(" ")]))
        total += output

    print(total)


        




