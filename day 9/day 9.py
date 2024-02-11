import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
from collections import deque
from functools import reduce

#
# Classes
#
class HeightMap:
    def __init__(self, map_string: str) -> None:
        width = map_string.find('\n') + 1
        self.tiles = {}
        for i, c in enumerate(map_string):
            if c == '\n': continue
            pos = i%width + i//width*1j
            self.tiles[pos] = int(c)

    def get_low_points_risks(self) -> int:
        all_tiles = set(self.tiles)
        risk_level = 0
        for t in self.tiles:
            neighbors = {t+1, t-1, t+1j, t-1j} & all_tiles
            if self.tiles[t] < min(self.tiles[nb] for nb in neighbors): risk_level += self.tiles[t]+1
        return risk_level
    
    def find_basins(self) -> list:
        all_tiles = set(self.tiles)
        explored = set()
        basins = []
        for t in self.tiles:
            if t in explored or self.tiles[t] == 9: continue

            this_basin = set()
            queue = deque([ t ])
            while len(queue) > 0:
                pos = queue.popleft()
                if pos in this_basin: continue
                this_basin.add(pos)
                neighbors = {pos+1, pos-1, pos+1j, pos-1j} & all_tiles
                neighbors_in_basin = {nb for nb in neighbors if self.tiles[nb] < 9}
                for nb in neighbors_in_basin: queue.append(nb)
            basins.append(len(this_basin))
            explored |= this_basin

        return basins

#
# Process input
#
heighmap = input_handling.read_from_file('day 9/input.txt', HeightMap)

print(f'Puzzle 1 solution is: {heighmap.get_low_points_risks()}')

basins = heighmap.find_basins()
basins.sort(reverse=True)

print(f'Puzzle 2 solution is: {reduce(lambda a, b: a * b, basins[:3])}')