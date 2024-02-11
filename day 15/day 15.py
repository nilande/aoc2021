import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
import heapq
from aoc_utils.set_renderer import TextRenderer

#
# Classes
#
class CavernMap:
    def __init__(self, map_string: str, tile_map: int = 1) -> None:
        width = map_string.find('\n') + 1
        height = -(len(map_string) // -width)
        self.tiles = {}
        for i, c in enumerate(map_string):
            if c == '\n': continue
            pos = i % width + i // width *1j
            num = int(c)
            for x in range(tile_map):
                for y in range(tile_map):
                    self.tiles[pos+(width-1)*x+height*y*1j] = (num + x + y - 1) % 9 + 1
        self.start = 0+0j
        self.finish = (width-1)*tile_map-1+(height*tile_map-1)*1j

    def get_path(self) -> tuple:
        id = 0
        queue = [ (0, id, self.start, []) ]
        explored = set()
        valid_tiles = set(self.tiles.keys())

        while len(queue) > 0:
            risk, _, pos, path = heapq.heappop(queue)
            if pos in explored: continue
            explored.add(pos)
            path.append(pos)
            if pos == self.finish: break
            neighbors = {pos+1, pos-1, pos+1j, pos-1j} & valid_tiles
            for nb in neighbors:
                id += 1
                heapq.heappush(queue, (risk+self.tiles[nb], id, nb, path.copy()))

        return risk, path


#
# Process input
#

#
# Puzzle 1
#
cavern_map = input_handling.read_from_file('day 15/input.txt', CavernMap)
risk, path = cavern_map.get_path()
tr = TextRenderer(cavern_map.tiles, path)
tr.draw(True)

print(f'Puzzle 1 solution is: {risk}')

#
# Puzzle 2
#
cavern_map = input_handling.read_from_file('day 15/input.txt', lambda x: CavernMap(x, 5))
risk, _ = cavern_map.get_path()
print(f'Puzzle 2 solution is: {risk}')
