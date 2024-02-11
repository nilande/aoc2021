import sys, os
sys.path.append(os.getcwd())
from aoc_utils.input_handling import read_lines_from_file

#
# Classes
#
class Line:
    def __init__(self, line_string: str) -> None:
        p0_str, p1_str = line_string.split(' -> ')
        x0, y0 = p0_str.split(',')
        x1, y1 = p1_str.split(',')
        self.p0 = int(x0)+int(y0)*1j
        self.p1 = int(x1)+int(y1)*1j

    def get_points(self, orthogonal_only: bool = True) -> list:
        delta = self.p1 - self.p0
        delta_x = abs(int(delta.real))
        delta_y = abs(int(delta.imag))
        if orthogonal_only and delta_x > 0 and delta_y > 0: return []
        steps = max(delta_x, delta_y)
        points = [ self.p0 ]
        for i in range(steps): points.append(self.p0 + (i+1)*delta/steps)
        return points

#
# Process input
#
lines = read_lines_from_file('day 5/input.txt', Line)

#
# Puzzle 1
#
points_dict = {}
for line in lines:
    line_points = line.get_points()
    for p in line_points:
        points_dict.setdefault(p, 0)
        points_dict[p] += 1

overlaps = sum(1 for p, v in points_dict.items() if v > 1)
print(f'Puzzle 1 solution is: {overlaps}')

#
# Puzzle 2
#
points_dict = {}
for line in lines:
    line_points = line.get_points(orthogonal_only = False)
    for p in line_points:
        points_dict.setdefault(p, 0)
        points_dict[p] += 1

overlaps = sum(1 for p, v in points_dict.items() if v > 1)
print(f'Puzzle 2 solution is: {overlaps}')
