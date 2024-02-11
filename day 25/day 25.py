import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling

#
# Classes
#
class SituationMap:
    def __init__(self, map_string: str) -> None:
        self.width = map_string.find('\n')
        self.height = -(len(map_string) // -(self.width+1))

        self.tiles_e = set()
        self.tiles_s = set()
        for i, c in enumerate(map_string):
            pos = i%(self.width+1) + i//(self.width+1)*1j
            match c:
                case '>': self.tiles_e.add(pos)
                case 'v': self.tiles_s.add(pos)

    def step(self) -> bool:
        tiles_occupied = self.tiles_e | self.tiles_s
        next_tiles_e = set()
        for p in self.tiles_e:
            next_p = p+1
            if next_p.real == self.width: next_p -= self.width
            next_tiles_e.add(next_p if next_p not in tiles_occupied else p)
        changed = self.tiles_e != next_tiles_e
        self.tiles_e = next_tiles_e

        tiles_occupied = self.tiles_e | self.tiles_s
        next_tiles_s = set()
        for p in self.tiles_s:
            next_p = p+1j
            if next_p.imag == self.height: next_p -= self.height*1j
            next_tiles_s.add(next_p if next_p not in tiles_occupied else p)
        changed |= self.tiles_s != next_tiles_s
        self.tiles_s = next_tiles_s

        return changed


#
# Process input
#
situation_map = input_handling.read_from_file('day 25/input.txt', SituationMap)

#
# Final puzzle
#
acc = 1
while situation_map.step(): acc += 1

print(f'Puzzle solution is: {acc}')