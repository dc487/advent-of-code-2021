import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

def print_paper(paper):
    for y in range(len(paper)):
        line = ""
        for x in range(len(paper[y])):
            if paper[y][x]:
                line += "#"
            else:
                line += "."
        print(line)

if __name__ == "__main__":
    input = load_input()

    paper = []
    for i in range(2000):
        paper.append([False] * 2000)

    index = 0
    while (input[index] != ""):
        parts = input[index].split(",")
        index += 1
        x = int(parts[0])
        y = int(parts[1])
        paper[y][x] = True

    index += 1
    fold = 0
    while (index < len(input)):
        parts = input[index].split("=")
        index += 1
        fold += 1
        fold_direction = parts[0]
        fold_number = int(parts[1])

        folded_paper = []
        if (fold_direction == "fold along x"):
             for y in range(len(paper)):
                folded_paper.append(paper[y][:fold_number])
                width = len(folded_paper[y])
                for x in range(width):
                    if (width + 1 + x >= len(paper[y])):
                        break
                    folded_paper[y][width - 1 - x] = folded_paper[y][width - 1 - x] or paper[y][width + 1 + x]

        elif(fold_direction == "fold along y"):
            folded_paper = paper[:fold_number]
            for y in range(fold_number):
                if (fold_number + 1 + y >= len(paper)):
                    break
                for x in range(len(paper[0])):
                    folded_paper[fold_number - 1 - y][x] = folded_paper[fold_number - 1 - y][x] or paper[fold_number + 1 + y][x]

        paper = folded_paper

        if (fold == 1):
            count = 0
            for y in range(len(paper)):
                for x in range(len(paper[y])):
                    if (paper[y][x]):
                        count += 1
            print(count)
    
    print_paper(paper)

        
