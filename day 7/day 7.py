import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling

#
# Process input
#
crab_positions = input_handling.read_from_file('day 7/input.txt', lambda x: list(map(int, x.split(','))))

#
# Puzzles 1 and 2
#
p1_fuels = []
p2_fuels = []
for x in range(min(crab_positions), max(crab_positions)+1):
    p1_fuels.append(sum(abs(p-x) for p in crab_positions))
    p2_fuels.append(sum(abs(p-x)*(abs(p-x)+1)//2 for p in crab_positions))

print(f'Puzzle 1 solution is: {min(p1_fuels)}')
print(f'Puzzle 2 solution is: {min(p2_fuels)}')