import functools

#
# Puzzle 1
#
class Die:
    def __init__(self) -> None:
        self.state = 7
        self.rolls = 0

    def roll(self) -> int:
        self.state = (self.state-1) % 10
        self.rolls += 3
        return self.state

class Player:
    def __init__(self, start: int) -> None:
        self.pos = start
        self.score = 0

    def roll_die(self, d: Die) -> bool:
        """Roll die three times. Return True if and only if player wins"""
        self.pos = (self.pos + d.roll() - 1) % 10 + 1
        self.score += self.pos
        # print(f'Player moves to space {self.pos} for a total score of {self.score}')
        return self.score >= 1000

d = Die()
# Configure according to puzzle input
p1 = Player(4)
p2 = Player(8)

while True:
    if p1.roll_die(d):
        print(f'Puzzle 1 solution is: {p2.score * d.rolls}')
        break
    if p2.roll_die(d):
        print(f'Puzzle 1 solution is: {p1.score * d.rolls}')
        break

#
# Puzzle 2
#
DICE_FREQ = {
    3: 1, # 111
    4: 3, # 112 121 211
    5: 6, # 122 212 221 113 131 311
    6: 7, # 123 132 213 231 312 321 222
    7: 6, # 133 313 331 223 232 322
    8: 3, # 332 323 233
    9: 1  # 333
}

@functools.cache
def count_win_universes(positions: tuple, scores: tuple) -> tuple:
    """Get the number of universes in which players 1 and 2 wins.
    Inputs:
    - positions: tuple containing player 1 and 2 positions
    - scores: tuple containing the scores for players 1 and 2"""
    p1_pos, p2_pos = positions
    p1_score, p2_score = scores

    if p2_score >= 21: return 0, 1 # PLayer 2 has won

    p1_wins = 0
    p2_wins = 0
    for roll, freq in DICE_FREQ.items():
        p1_new_pos = (p1_pos + roll - 1) % 10 + 1
        p1_new_score = p1_score + p1_new_pos

        # Now it is player 2's turn
        p2_sub_wins, p1_sub_wins = count_win_universes((p2_pos, p1_new_pos), (p2_score, p1_new_score))
        
        p1_wins += p1_sub_wins * freq
        p2_wins += p2_sub_wins * freq

    return p1_wins, p2_wins

# Configure according to puzzle input
print(f'Puzzle 2 solution is: {max(count_win_universes((4, 8), (0, 0)))}')