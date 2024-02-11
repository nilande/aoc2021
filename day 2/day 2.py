import sys, os
sys.path.append(os.getcwd())
from aoc_utils.input_handling import read_lines_from_file

#
# Process input
#
course = read_lines_from_file('day 2/input.txt', lambda x: x.split())

#
# Puzzle 1
#
pos = 0+0j
for step in course:
    match step:
        case ['forward', n]: pos += int(n)
        case ['down', n]: pos += int(n)*1j
        case ['up', n]: pos += int(n)*-1j

print(f'Puzzle 1 solution is: {int(pos.real) * int(pos.imag)}')

#
# Puzzle 2
#
pos = 0+0j
aim = 0
for step in course:
    match step:
        case ['forward', n]: pos += int(n)*(1+aim*1j)
        case ['down', n]: aim += int(n)
        case ['up', n]: aim -= int(n)

print(f'Puzzle 2 solution is: {int(pos.real) * int(pos.imag)}')