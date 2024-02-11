import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
import re, math

def test_trajectory(target: tuple, velocity: tuple) -> bool:
    x, y = (0, 0)
    dx, dy = velocity
    xmin, xmax, ymin, ymax = target
    while x < xmax and y > ymin:
        x += dx
        y += dy
        dx -= (dx > 0) - (dx < 0)
        dy -= 1
        if xmin <= x <= xmax and ymin <= y <= ymax: return True
    return False

#
# Process input
#
target = list(map(int, re.findall(r'target area: x=([-\d]+)\.\.([-\d]+), y=([-\d]+)\.\.([-\d]+)', input_handling.read_from_file('day 17/input.txt'))[0]))
xmin, xmax, ymin, ymax = target

#
# Puzzle 1
#

# We take for granted there is a dx that allows x velocity to become 0 in the target area
dxmin = int(-((math.sqrt(8*xmin+1)-1)//-2))
dxmax = int((math.sqrt(8*xmax+1)-1)//2)
assert(dxmin <= dxmax)

# Max y velocity is the velocity where the first y value below 0 is at the bottom of the target area
dymax = -ymin - 1
print(f'Puzzle 1 solution is: {dymax*(dymax+1)//2}')

#
# Puzzle 2
#
acc = 0
# Test trajectories where it takes at least two steps to reach target area
for dx in range(dxmin, -(xmax//-2)+1):
    for dy in range(ymin//2, dymax+1):
        if test_trajectory(target, (dx, dy)): acc += 1

# Count all velocities where target area is reached in one step
acc += (xmax-xmin+1)*(ymax-ymin+1)
print(f'Puzzle 2 solution is: {acc}')