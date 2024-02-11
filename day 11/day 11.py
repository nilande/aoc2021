import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling

#
# Classes
#
class Octopus:
    def __init__(self, energy_level: int) -> None:
        self.energy_level = energy_level

    def __repr__(self) -> str:
        return f'\033[1;97m{self.energy_level}\033[0m' if self.energy_level == 0 else f'{self.energy_level}'

    def set_neighbors(self, neighbors: set) -> None:
        self.neighbors = neighbors
    
    def raise_energy_level(self):
        self.energy_level += 1
        self.has_flashed = False

    def process_flashes(self, exposed: bool = False) -> int:
        if self.has_flashed: return 0
        if exposed: self.energy_level += 1
        if self.energy_level > 9:
            num_flashes = 1
            self.has_flashed = True
            self.energy_level = 0
            for nb in self.neighbors: num_flashes += nb.process_flashes(exposed = True)
            return num_flashes
        else: return 0

class OctopusMap:
    def __init__(self, map_string: str) -> None:
        width = map_string.find('\n') + 1
        height = -(len(map_string)//-width)
        self.octopi = {}
        for y in range(height):
            for x in range(width-1):
                self.octopi[x+y*1j] = Octopus(int(map_string[y*width + x]))
        for pos, octopus in self.octopi.items():
            neighbors = {pos+1, pos-1, pos-1+1j, pos+1j, pos+1+1j, pos-1-1j, pos-1j, pos+1-1j} & set(self.octopi)
            octopus.set_neighbors({self.octopi[nb] for nb in neighbors})
        self.width = width-1
        self.height = height

    def __repr__(self) -> str:
        map_string = ''
        for y in range(self.height):
            for x in range(self.width):
                pos = x+y*1j
                map_string += f'{self.octopi[pos]}'
            map_string += '\n'
        return map_string
    
    def step(self) -> int:
        flashes = 0
        for o in self.octopi.values(): o.raise_energy_level()
        for o in self.octopi.values(): flashes += o.process_flashes()
        return flashes

    

#
# Process input
#
octopus_map = input_handling.read_from_file('day 11/input.txt', OctopusMap)

#
# Puzzle 1 and 2
#
print(octopus_map)

acc = 0
i = 0
while True:
    i += 1
    flashes = octopus_map.step()
    acc += flashes
    if i == 100:
        print(octopus_map)
        print(f'Puzzle 1 solution is: {acc}')
    if flashes == 100:
        print(f'Puzzle 2 solution is: {i}')
        break

