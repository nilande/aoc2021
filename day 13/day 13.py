import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
from aoc_utils.set_renderer import BrailleRenderer

#
# Process input
#
dot_string, instruction_string = input_handling.read_from_file('day 13/input.txt', lambda x: x.split('\n\n'))

#
# Puzzle 1
#
dots = set()
for x, y in map(lambda x: x.split(','), dot_string.splitlines()):
    dots.add(int(x)+int(y)*1j)

for i, instruction in enumerate(instruction_string.splitlines()):
    match instruction[11:].split('='):
        case ['x', n]: dots = {x if x.real<int(n) else x+2*(int(n)-x.real) for x in dots}
        case ['y', n]: dots = {x if x.imag<int(n) else x+2j*(int(n)-x.imag) for x in dots}
    if i == 0: print(f'Puzzle 1 solution is: {len(dots)}')

print(f'Puzzle 2 solution is:')
BrailleRenderer(dots).draw()
