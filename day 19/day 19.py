import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
import numpy as np
from itertools import permutations, product

#
# Classes
#
class Scanner:
    def __init__(self, init_string: str) -> None:
        lines = init_string.splitlines()
        self.id = int(lines[0][12:-4])
        self.beacons = np.zeros((len(lines)-1, 3), dtype=np.int16)
        self.scanners = np.array([0, 0, 0])
        for i, b in enumerate(lines[1:]):
            self.beacons[i,:] = list(map(int, b.split(',')))

    def __repr__(self) -> str:
        return f'Scanner {self.id}'
    
    def merge_if_overlap(self, other: 'Scanner', rot: np.ndarray):
        other_rotated = other.beacons @ rot
        offsets = {}
        for b1, b2 in product(self.beacons, other_rotated):
            offset = tuple(b1-b2)
            offsets.setdefault(offset, 0)
            offsets[offset] += 1
        offsets = [k for k, v in offsets.items() if v >= 12]

        if len(offsets) == 1:
            beacon_list = self.beacons.tolist()
            for b in other_rotated+offsets[0]:
                if not list(b) in beacon_list:
                    self.beacons = np.vstack([self.beacons, b])
            self.scanners = np.vstack([self.scanners, other.scanners @ rot + offsets[0]])
            return True
        return False

#
# Helper functions
#
def get_rotation_matrices():
    """Get the 24 possible rotation matrices (facing 6 directions with 4 possible orientations each)"""
    rotations = []
    identity = np.identity(3, dtype=np.int16)
    for p in permutations(identity):
        P = np.array(p)
        for s in product([-1, 1], repeat=3):
            S = np.diag(s)
            M = S @ P
            if np.linalg.det(M) == 1: rotations.append(M)
    return rotations

#
# Process input
#
scanners = input_handling.read_from_file('day 19/input.txt', lambda x: list(map(Scanner, x.split('\n\n'))))

#
# Puzzle 1
#
rotations = get_rotation_matrices()
while len(scanners) > 1:
    for s1, s2, r in product(scanners, scanners, rotations):
        if s1.id >= s2.id: continue
        if s1.merge_if_overlap(s2, r):
            scanners.remove(s2)
            break

print(f'Puzzle 1 solution is: {len(scanners[0].beacons)}')

#
# Puzzle 2
#
scanners = scanners[0].scanners
distances = []
for i, s1 in enumerate(scanners):
    for s2 in scanners[i+1:]:
        distances.append(sum(abs(s1-s2)))

print(f'Puzzle 2 solution is: {max(distances)}')        