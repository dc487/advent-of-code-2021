import pathlib

class _BingoCell:
    def __init__(self, number):
        self.number = int(number)
        self.marked = False
    
    def mark(self, number):
        if (self.number == number):
            self.marked = True

class _BingoCard:
    def __init__(self, card):
        self.rows = [[_BingoCell(y) for y in x.strip(" ").replace("  ", " ").split(" ")] for x in card.splitlines()]

    def mark(self, number):
        for row in self.rows:
            for cell in row:
                cell.mark(number)

    def has_won(self):
        for index in range(5):
            row = self.rows[index]
            if len([x for x in row if x.marked]) == 5:
                return True
            
            column = [x[index] for x in self.rows]
            if len([x for x in column if x.marked]) == 5:
                return True

        return False

    def calculate_score(self, winning_number):
        total = 0
        for row in self.rows:
            for cell in row:
                if not cell.marked:
                    total += cell.number

        return total * winning_number


def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n")

if __name__ == "__main__":
    input = load_input()

    random_order = [int(x) for x in input.splitlines()[0].split(",")]

    bingo_cards = [_BingoCard(x.strip("\n")) for x in "\n".join(input.splitlines()[1::]).split("\n\n")]

    score = 0
    for number in random_order:
        for bingo_card in bingo_cards:
            bingo_card.mark(number)
            if (bingo_card.has_won()):
                score = bingo_card.calculate_score(number)
                break
        else:
            continue
        break
    
    print(score)


    bingo_cards = [_BingoCard(x.strip("\n")) for x in "\n".join(input.splitlines()[1::]).split("\n\n")]

    score = 0
    for number in random_order:
        for bingo_card in bingo_cards:
            bingo_card.mark(number)
        for bingo_card in bingo_cards:
            if (bingo_card.has_won()):
                if len(bingo_cards) == 1:
                    score = bingo_card.calculate_score(number)
                    break

                bingo_cards.remove(bingo_card)
        else:
            continue
        break

    print(score)