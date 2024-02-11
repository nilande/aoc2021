import sys, os
sys.path.append(os.getcwd())
from aoc_utils.input_handling import read_from_file

#
# Classes
#
class DrawSequence:
    def __init__(self, sequence_string: str) -> None:
        self.sequence = list(map(int, sequence_string.split(',')))

    def draw(self) -> int:
        return self.sequence.pop(0)

class BingoBoard:
    def __init__(self, board_string: str) -> None:
        self.board = list(map(int, board_string.split()))
        self.drawn = set()
        self.bingo = False

    def hear_drawn(self, drawn: int):
        self.drawn.add(drawn)
        result = False
        for r in range(5): # Check rows
            if all(n in self.drawn for n in self.board[r*5:(r+1)*5]): result = True
        for c in range(5): # Check cols
            if all(n in self.drawn for n in self.board[c:c+21:5]): result = True
        self.bingo = result
        return result, sum(n for n in self.board if n not in self.drawn)

#
# Process input
#
content = read_from_file('day 4/input.txt').split('\n\n')

draw_sequence = DrawSequence(content[0])

bingo_boards = list(map(lambda x: BingoBoard(x), content[1:]))

#
# Puzzle 1 & 2
#
p1_solution, p2_solution = None, None
while len(bingo_boards) > 0:
    drawn = draw_sequence.draw()
    for board in bingo_boards:
        bingo, score = board.hear_drawn(drawn)
        if bingo:
            if p1_solution is None: p1_solution = drawn * score
            if len(bingo_boards) == 1: p2_solution = drawn * score
    bingo_boards = [b for b in bingo_boards if not b.bingo]

print(f'Puzzle 1 solution is: {p1_solution}')
print(f'Puzzle 2 solution is: {p2_solution}')
