import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling, set_renderer

#
# Classes
#
class Image:
    def __init__(self, data: tuple) -> None:
        algorithm, image_data = data
        self.algorithm = algorithm.replace('.', '0').replace('#','1')
        self.image = {}
        for y, row in enumerate(image_data.splitlines()):
            for x, c in enumerate(row):
                pos = x + y*1j
                match c:
                    case '#': self.image[pos] = '1'
                    case '.': self.image[pos] = '0'
        self.image_bg = '0'

    def __get_bits(self, pos: complex) -> int:
        bits = ''
        for y in range(-1, 2):
            for x in range(-1, 2):
                offset = x + y*1j
                if pos+offset in self.image:
                    bits += self.image[pos+offset]
                else:
                    bits += self.image_bg
        return int(bits, 2)
    
    def __get_bg_bits(self) -> int:
        return int(self.image_bg * 9, 2)

    def draw(self) -> int:
        pixels = {k for k, v in self.image.items() if v == '1'}
        br = set_renderer.BrailleRenderer(pixels)
        br.draw()
        return len(pixels)

    def enhance(self) -> None:
        xs = [int(x.real) for x in self.image.keys()]
        ys = [int(x.imag) for x in self.image.keys()]
        new_image = {}
        for y in range(min(ys)-1, max(ys)+2):
            for x in range(min(xs)-1, max(xs)+2):
                pos = x + y*1j
                bits = self.__get_bits(pos)
                new_image[pos] = self.algorithm[bits]
        self.image = new_image
        self.image_bg = self.algorithm[self.__get_bg_bits()]
        

#
# Process input
#
image = input_handling.read_from_file('day 20/input.txt', lambda x: Image(x.split('\n\n')))

#
# Puzzle 1
#
image.enhance()
image.enhance()
pixel_count = image.draw()
print(f'Puzzle 1 solution is: {pixel_count}')

#
# Puzzle 2
#
for i in range(48):
    image.enhance()
pixel_count = image.draw()
print(f'Puzzle 2 solution is: {pixel_count}')
