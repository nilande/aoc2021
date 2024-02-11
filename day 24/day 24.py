import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
import itertools, math

#
# Helper functions
#
def test_number(num_stack: list, instructions: list) -> dict:
    variables = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0
    }

    for i in instructions:
        match i.split():
            case ['inp', a]:
                if len(num_stack) == 0: return variables, 0 if variables['z'] == 0 else int(-(math.log(variables['z'], 26)//-1))
                variables[a] = num_stack.pop(0)
            case ['mul', a, b]:
                variables[a] *= variables[b] if b in variables else int(b)
            case ['eql', a, b]:
                variables[a] = int(variables[a] == variables[b]) if b in variables else int(variables[a] == int(b))
            case ['add', a, b]:
                variables[a] += variables[b] if b in variables else int(b)
            case ['div', a, b]:
                variables[a] //= variables[b] if b in variables else int(b)
            case ['mod', a, b]:
                variables[a] %= variables[b] if b in variables else int(b)
            case _:
                print(f'Unknown instruction {i}')

    return variables, 0 if variables['z'] == 0 else int(-(math.log(variables['z'], 26)//-1))

#
# Process input
#
instructions = input_handling.read_lines_from_file('day 24/input.txt')

#
# Puzzle 1 and 2
#
arglist = [()]

for i in range(14):
    results = []
    for test in [(*x,y) for x in arglist for y in range(1, 10)]:
        _, length = test_number(list(test), instructions)
        results.append((test, length))
    min_length = min(l for t, l in results)
    arglist = [t for t, l in results if l == min_length]
    print(f'After {i+1} iterations, list is {len(arglist)} long, max is {max(arglist)} and min is {min(arglist)}')

print(f'Puzzle 1 solution is: {max(arglist)}')
print(f'Puzzle 2 solution is: {min(arglist)}')