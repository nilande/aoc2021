
import sys, os
sys.path.append(os.getcwd())
from aoc_utils.input_handling import read_lines_from_file

#
# Process input
#
lines = read_lines_from_file('day 1/input.txt', int)

#
# Puzzle 1
#
acc = 0
for i in range(len(lines)-1):
    if lines[i+1]>lines[i]: acc += 1
print(f'Puzzle 1 solution is: {acc}')

acc = 0
for i in range(len(lines)-3):
    if sum(lines[i+1:i+4]) > sum(lines[i:i+3]): acc += 1
print(f'Puzzle 2 solution is: {acc}')