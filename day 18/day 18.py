import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
from copy import deepcopy

#
# Classes
#
class SnailfishNumber:
    def __init__(self, number_string: str) -> None:
        self.value = None
        self.left = None
        self.right = None

        if number_string is None: return
        elif number_string.isdigit():
            self.value = int(number_string)
        else:
            number_string = number_string[1:-1]
            level = 0
            for i, c in enumerate(number_string):
                match c:
                    case '[': level += 1
                    case ']': level -= 1
                    case ',' if level == 0:
                        left = number_string[:i]
                        right = number_string[i+1:]
                        break
            self.left = SnailfishNumber(left)
            self.right = SnailfishNumber(right)

    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]' if self.value is None else f'{self.value}'
    
    def add(self, other: 'SnailfishNumber') -> 'SnailfishNumber':
        result = SnailfishNumber(None)
        result.left = self
        result.right = other
        return result

    def get_inorder_sequence(self) -> list:
        if self.value is not None: return [ self ]
        else: return self.left.get_inorder_sequence() + self.right.get_inorder_sequence()

    def get_magnitude(self) -> int:
        if self.value is not None: return self.value
        return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()

    def reduce(self):
        while True:
            result = False
            while True:
                inorder_sequence = self.get_inorder_sequence()
                exploded = self.try_explode(inorder_sequence)
                result |= exploded
                if exploded == False: break
                # print(f'After explode: {self}')
            split = self.try_split()
            result |= split
            # if split: print(f'After split: {self}')
            if not result: break

    def try_explode(self, inorder_sequence: list, nest_level: int = 0) -> bool:
        if self.value is not None: return False
        elif nest_level == 4:
            left_index = inorder_sequence.index(self.left)
            right_index = inorder_sequence.index(self.right)
            assert(left_index + 1 == right_index)
            if left_index > 0: inorder_sequence[left_index-1].value += self.left.value
            if right_index < len(inorder_sequence)-1: inorder_sequence[right_index+1].value += self.right.value
            self.value = 0
            self.left = None
            self.right = None
            return True
        else:
            exploded = self.left.try_explode(inorder_sequence, nest_level+1)
            if not exploded: exploded = self.right.try_explode(inorder_sequence, nest_level+1)
            return exploded

    def try_split(self) -> bool:
        if self.value is not None:
            if self.value < 10: return False
            else:
                self.left = SnailfishNumber(None)
                self.left.value = self.value // 2
                self.right = SnailfishNumber(None)
                self.right.value = self.value - self.left.value
                self.value = None
                return True
        else:
            split = self.left.try_split()
            if not split: split = self.right.try_split()
            return split

#
# Process input
#
numbers = input_handling.read_lines_from_file('day 18/input.txt', SnailfishNumber)
numbers_copy = deepcopy(numbers)

#
# Puzzle 1
#
new_number = numbers[0]
for n in numbers[1:]:
    new_number = new_number.add(n)
    new_number.reduce()

print(f'Puzzle 1 solution is: {new_number.get_magnitude()}')

#
# Puzzle 2
#
largest_magnitude = None
for a in numbers_copy:
    for b in numbers_copy:
        if a == b: continue
        new_a = deepcopy(a)
        new_b = deepcopy(b)
        new_number = new_a.add(new_b)
        new_number.reduce()
        magnitude = new_number.get_magnitude()
        if largest_magnitude is None or magnitude > largest_magnitude: largest_magnitude = magnitude

print(f'Puzzle 2 solution is: {largest_magnitude}')