import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling

#
# Process input
#
lines = input_handling.read_lines_from_file('day 10/input.txt')

CHUNK_CLOSINGS = {'(': ')', '[': ']', '{': '}', '<': '>'}
CHUNK_OPENINGS = set(CHUNK_CLOSINGS.keys())
CHUNK_POINTS = {')': 3, ']': 57, '}': 1197, '>': 25137}
CLOSING_SCORE = {')': 1, ']': 2, '}': 3, '>': 4}

#
# Puzzle 1 and 2
#
p1_solution = 0
p2_solutions = []
incomplete_lines = []
for line in lines:
    stack = []
    for c in line:
        if c in CHUNK_OPENINGS: stack.append(c)
        else:
            c_exp = CHUNK_CLOSINGS[stack.pop()]
            if c_exp != c:
                p1_solution += CHUNK_POINTS[c]
                break
    else:
        line_points = 0
        for s in stack[::-1]:
            line_points *= 5
            line_points += CLOSING_SCORE[CHUNK_CLOSINGS[s]]
        p2_solutions.append(line_points)
        
print(f'Puzzle 1 solution is: {p1_solution}')

p2_solutions.sort()
print(f'Puzzle 2 solution is: {p2_solutions[len(p2_solutions)//2]}')
