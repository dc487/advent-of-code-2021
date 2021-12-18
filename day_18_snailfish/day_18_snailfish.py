import pathlib
import math

class _Pair:
    def __init__(self, number_string, depth = 0, parent = None):
        self.depth = depth
        self.parent = parent

        # This should always be a square bracket
        number_string.pop(0)

        if number_string[0] == '[':
            self.left = _Pair(number_string, depth + 1, self)
        else:
            left_string = number_string.pop(0)
            while number_string[0] != ',':
                left_string += number_string.pop(0)
            self.left = int(left_string)

        # This will always be a comma
        number_string.pop(0)

        if number_string[0] == '[':
            self.right = _Pair(number_string, depth + 1, self)
        else:
            right_string = number_string.pop(0)
            while number_string[0] != ']':
                right_string += number_string.pop(0)
            self.right = int(right_string)

        # This should always be a square bracket 
        number_string.pop(0)

    def to_string(self):
        string = '['
        if type(self.left) == int:
            string += str(self.left)
        else:
            string += self.left.to_string()

        string += ','

        if type(self.right) == int:
            string += str(self.right)
        else:
            string += self.right.to_string()

        string += ']'
        return string

    def add(self, other):
        added_pair = _Pair(list('[' + self.to_string() + ',' + other.to_string() + ']'))
        while True:
            if added_pair.explode():
                continue
            if not added_pair.split():
                break

        return added_pair

    def add_to_first_left_number_from_parent(self, x):
        if type(self.right) == int:
            self.right += x
            return True
        elif self.right.add_to_first_left_number_from_parent(x):
            return True
        elif type(self.left) == int:
            self.left += x
            return True
        elif self.left.add_to_first_left_number_from_parent(x):
            return True
        else:
            return False

    def add_to_first_left_number_from_child(self, child, x):
        if self.right == child:
            if type(self.left) == int:
                self.left += x
                return True
            elif self.left.add_to_first_left_number_from_parent(x):
                return True
        elif self.left == child:
            if self.parent is not None:
                if self.parent.add_to_first_left_number_from_child(self, x):
                    return True
        
        return False

    def add_to_first_right_number_from_parent(self, x):
        if type(self.left) == int:
            self.left += x
            return True
        elif self.left.add_to_first_right_number_from_parent(x):
            return True
        elif type(self.right) == int:
            self.right += x
            return True
        elif self.right.add_to_first_right_number_from_parent(x):
            return True
        else:
            return False

    def add_to_first_right_number_from_child(self, child, x):
        if self.left == child:
            if type(self.right) == int:
                self.right += x
                return True
            elif self.right.add_to_first_right_number_from_parent(x):
                return True
        elif self.right == child:
            if self.parent is not None:
                if self.parent.add_to_first_right_number_from_child(self, x):
                    return True
        
        return False

    def explode(self):
        if self.depth >= 3:
            if type(self.left) != int:
                exploding = self.left
                self.left = 0
                if self.parent is not None:
                    self.parent.add_to_first_left_number_from_child(self, exploding.left)

                if type(self.right) == int:
                    self.right += exploding.right
                elif not self.right.add_to_first_right_number_from_parent(exploding.right):
                    if self.parent is not None:
                        return self.parent.add_to_first_right_number_from_child(self, exploding.right)

                return True
            
            if type(self.right) != int:
                exploding = self.right
                self.right = 0
                if self.parent is not None:
                    self.parent.add_to_first_right_number_from_child(self, exploding.right)

                if type(self.left) == int:
                    self.left += exploding.left
                elif not self.left.add_to_first_left_number_from_parent(exploding.left):
                    if self.parent is not None:
                        return self.parent.add_to_left_right_number_from_child(self, exploding.left)

                return True

            return False
        else:
            if type(self.left) != int and self.left.explode():
                return True
            elif type(self.right) != int and self.right.explode():
                return True

            return False

    def split(self):
        if type(self.left) == int:
            if self.left > 9:
                left_split = math.floor(self.left / 2)
                right_split = math.ceil(self.left / 2)
                self.left = _Pair(list('[' + str(left_split) + ',' + str(right_split) + ']'), self.depth + 1, self)
                return True
        elif self.left.split():
            return True

        if type(self.right) == int:
            if self.right > 9:
                left_split = math.floor(self.right / 2)
                right_split = math.ceil(self.right / 2)
                self.right = _Pair(list('[' + str(left_split) + ',' + str(right_split) + ']'), self.depth + 1, self)
                return True
        elif self.right.split():
            return True

        return False

    def get_magnitude(self):
        left_magnitude = 0
        if type(self.left) == int:
            left_magnitude = self.left
        else:
            left_magnitude = self.left.get_magnitude()

        right_magnitude = 0
        if type(self.right) == int:
            right_magnitude = self.right
        else:
            right_magnitude = self.right.get_magnitude()

        return 3 * left_magnitude + 2 * right_magnitude


def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

if __name__ == "__main__":
    input = load_input()

    snailfish_numbers = []
    for line in input:
        snailfish_numbers.append(_Pair(list(line)))

    current_total = snailfish_numbers[0]
    for i in range(1, len(snailfish_numbers)):
        current_total = current_total.add(snailfish_numbers[i])

    print(current_total.get_magnitude())

    largest_magnitude = 0
    for i in range(len(snailfish_numbers)):
        for j in range(len(snailfish_numbers)):
            if i != j:
                added_number = snailfish_numbers[i].add(snailfish_numbers[j])
                magnitude = added_number.get_magnitude()
                if magnitude > largest_magnitude:
                    largest_magnitude = magnitude

    print(largest_magnitude)

    
