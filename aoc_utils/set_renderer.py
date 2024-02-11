#
# Classes
#
class BrailleRenderer:
    """Class that renders sets of points in complex coordinates using Braille unicode characters
    x is the real value (right is positive) and y is the imaginary part (down is positive)"""
    def __init__(self, data: set) -> None:
        self.data = data
        self.prev_draw_lines = 0

    def __mask_to_braille(self, mask: int) -> int:
        braille_masks = [0x1, 0x2, 0x4, 0x40, 0x8, 0x10, 0x20, 0x80]
        braille_mask = 0
        for i in range(8):
            if mask & 1 << i: braille_mask |= braille_masks[i]
        return chr(0x2800 + braille_mask)

    def render(self) -> tuple:
        """Renders the contents of a set and returns a tuple containing the rendered string and
        the number of lines in the rendered string"""
        cols = [int(x.real) for x in self.data]
        rows = [int(x.imag) for x in self.data]
        string = ''
        lines = 0
        for r in range(min(rows)//4, -(max(rows)//-4)+1):
            y = r * 4
            for c in range(min(cols)//2, -(max(cols)//-2)+1):
                x = c * 2
                char_mask = 0
                for i in range(8):
                    if x+i//4 + (y+i%4)*1j in self.data: char_mask |= 1<<i
                string += self.__mask_to_braille(char_mask)
            string += '\n'
            lines += 1
        return string, lines
    
    def draw(self, reset_draw_lines: bool = False) -> None:
        """Wrapper function for render, but the results are also printed. When called multiple
        times, it moves cursor up to compensate for the lines drawn the previous time"""
        string, draw_lines = self.render()
        if not reset_draw_lines and self.prev_draw_lines > 0:
            print(f'\033[{self.prev_draw_lines}A{string}', end='')
        else:
            print(f'{string}', end='')
        self.prev_draw_lines = draw_lines

class TextRenderer:
    """Class that renders sets of points in complex coordinates using a dictionary with coordinates
    and symbols to use. Also has ability to highlight a set of cooridnates, for intance a path"""
    def __init__(self, data: dict, highlight: set = None) -> None:
        self.data = data
        self.highlight = highlight
        self.prev_draw_lines = 0

    def render(self, highlight: bool = False) -> tuple:
        """Renders the contents of a set and returns a tuple containing the rendered string and
        the number of lines in the rendered string"""
        cols = [int(x.real) for x in self.data]
        rows = [int(x.imag) for x in self.data]
        string = ''
        lines = 0
        for r in range(min(rows), max(rows)+1):
            for c in range(min(cols), max(cols)+1):
                pos = c+r*1j
                string += f'\033[31m{self.data[pos]}\033[0m' if highlight and pos in self.highlight else f'{self.data[pos]}'
            string += '\n'
            lines += 1
        return string, lines
    
    def draw(self, highlight: bool = False, reset_draw_lines: bool = False) -> None:
        """Wrapper function for render, but the results are also printed. When called multiple
        times, it moves cursor up to compensate for the lines drawn the previous time"""
        string, draw_lines = self.render(highlight)
        if not reset_draw_lines and self.prev_draw_lines > 0:
            print(f'\033[{self.prev_draw_lines}A{string}', end='')
        else:
            print(f'{string}', end='')
        self.prev_draw_lines = draw_lines
