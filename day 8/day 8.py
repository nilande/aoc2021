import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
from itertools import permutations

#
# Process input
#
signal_patterns = input_handling.read_lines_from_file('day 8/input.txt', lambda x: list(map(lambda y: y.split(), x.split(' | '))))

#
# Puzzle 1
#
acc = 0
for _, four_digits in signal_patterns:
    acc += sum(1 for n in four_digits if len(n) in (2, 4, 3, 7))

print(f'Puzzle 1 solution is: {acc}')

#
# Puzzle 2
#
DIGITS = {
    0: {'a', 'b', 'c', 'e', 'f', 'g'},
    1: {'c', 'f'},
    2: {'a', 'c', 'd', 'e', 'g'},
    3: {'a', 'c', 'd', 'f', 'g'},
    4: {'b', 'c', 'd', 'f'},
    5: {'a', 'b', 'd', 'f', 'g'},
    6: {'a', 'b', 'd', 'e', 'f', 'g'},
    7: {'a', 'c', 'f'},
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    9: {'a', 'b', 'c', 'd', 'f', 'g'}  
}
BASELINE = ord('a')

def remap_elements(digit_elements: set, remapping: tuple) -> set:
    remapped_elements = set()
    for element in digit_elements:
        remapped_elements.add(remapping[ord(element)-BASELINE])
    return remapped_elements

def identify_digit(digit_elements: set, remapping: tuple) -> int:
    remapped_digit = remap_elements(digit_elements, remapping)
    return sum(k for k, v in DIGITS.items() if  v == remapped_digit)

original = 'abcdefg'
acc = 0
for all_digits, four_digits in signal_patterns:
    for remapping in permutations(original, 7):
        for digit in all_digits:
            remapped_digit = remap_elements(set(digit), remapping)
            if sum(1 for _, v in DIGITS.items() if  v == remapped_digit) == 0: break
        else: # A valid remapping for this pattern has been found. Process the digits
            number = 0
            for d in four_digits:
                number *= 10
                number += identify_digit(set(d), remapping)
            acc += number
            break

print(f'Puzzle 2 solution is: {acc}')
            