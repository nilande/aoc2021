import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
from collections import deque

#
# Classes
#
class Cave:
    SMALL = 0
    BIG = 1

    def __init__(self, name: str) -> None:
        self.name = name
        self.connections = set()
        self.type = Cave.BIG if name.isupper() else Cave.SMALL

    def __repr__(self) -> str:
        return self.name

    def connect(self, other: 'Cave') -> None:
        self.connections.add(other)


class CaveMap:
    def __init__(self, map_string: str) -> None:
        self.caves = {}
        for c1, c2 in map(lambda x: x.split('-'), map_string.splitlines()):
            if not c1 in self.caves: self.caves[c1] = Cave(c1)
            if not c2 in self.caves: self.caves[c2] = Cave(c2)
            self.caves[c1].connect(self.caves[c2])
            self.caves[c2].connect(self.caves[c1])

    def check_path(self, path: list, p2_mode) -> bool:
        if path.count(self.caves['start']) > 1: return False
        nodes = {x for x in path if x.type == Cave.SMALL}
        node_counts = [path.count(x) for x in nodes]
        node_counts.sort(reverse=True)
        if not p2_mode: return node_counts[0] == 1
        else: return node_counts[0] <= 2 and all(x == 1 for x in node_counts[1:])


    def get_distinct_paths(self, p2_mode: bool = False) -> int:
        queue = deque([ (self.caves['start'], []) ])
        paths = []

        while len(queue) > 0:
            cave, path = queue.popleft()
            path.append(cave)
            if not self.check_path(path, p2_mode): continue
            if cave == self.caves['end']:
                paths.append(path)
                continue
            for connection in cave.connections:
                queue.append((connection, path.copy()))

        return paths





#
# Process input
#
cave_map = input_handling.read_from_file('day 12/input.txt', CaveMap)

#
# Puzzle 1
#
print(f'Puzzle 1 solution is: {len(cave_map.get_distinct_paths())}')

#
# Puzzle 2
#
print(f'Puzzle 2 solution is: {len(cave_map.get_distinct_paths(p2_mode = True))}')