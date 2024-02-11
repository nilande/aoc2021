import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
import re

#
# Classes
#
class Cuboid:
    def __init__(self, coords) -> None:
        if type(coords) is tuple:
            (self.x_min, self.y_min, self.z_min), (self.x_max, self.y_max, self.z_max) = coords
        elif type(coords) is str:
            self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max = tuple(map(int, re.findall(r'x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)', coords)[0]))

    def __repr__(self) -> str:
        return f'x={self.x_min}..{self.x_max},y={self.y_min}..{self.y_max},z={self.z_min}..{self.z_max}'

    def is_in_limited_area(self) -> bool:
        return -50 <= self.x_min <= self.x_max <= 50 and -50 <= self.y_min <= self.y_max <= 50 and -50 <= self.z_min <= self.z_max <= 50

    def get_overlap(self, other: 'Cuboid') -> 'Cuboid':
        if self.x_min <= other.x_max and other.x_min <= self.x_max and self.y_min <= other.y_max and other.y_min <= self.y_max and self.z_min <= other.z_max and other.z_min <= self.z_max:
            return Cuboid(((max(self.x_min, other.x_min), max(self.y_min, other.y_min), max(self.z_min, other.z_min)), (min(self.x_max, other.x_max), min(self.y_max, other.y_max), min(self.z_max, other.z_max))))
        else:
            return None

    def get_volume(self) -> int:
        return (self.x_max - self.x_min + 1) * (self.y_max - self.y_min + 1) * (self.z_max - self.z_min + 1)

    def fragment_cuboids(self, other: 'Cuboid') -> list:
        fragments = []
        if other.z_max < self.z_max:  # Back
            fragments.append(Cuboid(((self.x_min, self.y_min, other.z_max + 1), (self.x_max, self.y_max, self.z_max))))
        if self.z_min < other.z_min:  # Front
            fragments.append(Cuboid(((self.x_min, self.y_min, self.z_min), (self.x_max, self.y_max, other.z_min - 1))))
        if other.y_max < self.y_max:  # Top
            fragments.append(Cuboid(((self.x_min, other.y_max + 1, max(self.z_min, other.z_min)), (self.x_max, self.y_max, min(self.z_max, other.z_max)))))
        if self.y_min < other.y_min:  # Bottom
            fragments.append(Cuboid(((self.x_min, self.y_min, max(self.z_min, other.z_min)), (self.x_max, other.y_min - 1, min(self.z_max, other.z_max)))))
        if self.x_min < other.x_min:  # Left
            fragments.append(Cuboid(((self.x_min, max(self.y_min, other.y_min), max(self.z_min, other.z_min)), (other.x_min - 1, min(self.y_max, other.y_max), min(self.z_max, other.z_max)))))
        if other.x_max < self.x_max:  # Right
            fragments.append(Cuboid(((other.x_max + 1, max(self.y_min, other.y_min), max(self.z_min, other.z_min)), (self.x_max, min(self.y_max, other.y_max), min(self.z_max, other.z_max)))))
        return fragments

#
# Process input
#
steps = input_handling.read_lines_from_file('day 22/input.txt')

#
# Puzzles 1 and 2
#
active_cuboids = []
for step in steps:
    action, coords = step.split()
    cuboid = Cuboid(coords)
    next_active_cuboids = []
    for ac in active_cuboids:
        overlap = ac.get_overlap(cuboid)
        if overlap is not None:
            for fragment in ac.fragment_cuboids(overlap): next_active_cuboids.append(fragment)
        else: next_active_cuboids.append(ac)
    if action == 'on': next_active_cuboids.append(cuboid)
    active_cuboids = next_active_cuboids

print(f'Processing {len(steps)} steps resulted in {len(active_cuboids)} cuboid fragments...')

p1_acc = 0
p2_acc = 0
for ac in active_cuboids:
    volume = ac.get_volume()
    if ac.is_in_limited_area(): p1_acc += volume
    p2_acc += volume

print(f'Puzzle 1 solution is: {p1_acc}')
print(f'Puzzle 2 solution is: {p2_acc}')