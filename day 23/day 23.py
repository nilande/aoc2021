import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling
from collections import deque
import heapq, time

#
# Constants
#
ALLOWED_MOVES_PART_1 = {
    1: 0b1101010101110001000,
    2: 0b1101010101101000100,
    3: 0b1101010101100100010,
    4: 0b1101010101100010001
}
ALLOWED_MOVES_PART_2 = {
    1: 0b110101010111000100010001000,
    2: 0b110101010110100010001000100,
    3: 0b110101010110010001000100010,
    4: 0b110101010110001000100010001
}
NEIGHBORS_PART_1 = [
    [4],
    [5],
    [6],
    [7],
    [0, 10],
    [1, 12],
    [2, 14],
    [3, 16],
    [9],
    [8, 10],
    [4, 9, 11],
    [10, 12],
    [5, 11, 13],
    [12, 14],
    [6, 13, 15],
    [14, 16],
    [7, 15, 17],
    [16, 18],
    [17]
]
NEIGHBORS_PART_2 = [
    [4],
    [5],
    [6],
    [7],
    [0, 8],
    [1, 9],
    [2, 10],
    [3, 11],
    [4, 12],
    [5, 13],
    [6, 14],
    [7, 15],
    [8, 18],
    [9, 20],
    [10, 22],
    [11, 24],
    [17],
    [16, 18],
    [12, 17, 19],
    [18, 20],
    [13, 19, 21],
    [20, 22],
    [14, 21, 23],
    [22, 24],
    [15, 23, 25],
    [24, 26],
    [25]
]

#
# Helper functions 
#
def state_from_string(input_string: str) -> int:
    result = 0
    for c in input_string:
        match c:
            case '.': result <<= 3
            case 'A': result = (result << 3) + 1
            case 'B': result = (result << 3) + 2
            case 'C': result = (result << 3) + 3
            case 'D': result = (result << 3) + 4
    return result

def get_possible_moves_for(state: int, start_pos: int, amphipod: int, mode: int) -> list:
    """Get possible moves for one particular amphipod at a particular position"""
    queue = deque([ (start_pos, 0) ])
    explored = set()
    moves = []

    while len(queue) > 0:
        pos, cost = queue.popleft()
        if pos in explored: continue
        explored.add(pos)
        if mode == 1:
            if ALLOWED_MOVES_PART_1[amphipod] & 1 << pos and cost > 0:
                invalid = False

                # Check rule #2 - don't move into a room with dissimilar amphipods further in that room
                if pos < 8 and pos >= 4 and ((state >> (pos-4)*3)) & 0o7 != amphipod: invalid = True

                # Check rule #3 - don't move from one spot in the hallway to another in the hallway
                if start_pos >= 8 and pos >= 8: invalid = True

                if not invalid: moves.append((state | amphipod << pos*3, cost))

            neighbors = NEIGHBORS_PART_1[pos]
        elif mode == 2:
            if ALLOWED_MOVES_PART_2[amphipod] & 1 << pos and cost > 0:
                invalid = False

                # Check rule #2 - don't move into a room with dissimilar amphipods further in that room
                if pos < 16 and pos >= 4:
                    pos_copy = pos - 4
                    while pos_copy > 0:
                        if (state >> (pos_copy)*3) & 0o7 != amphipod:
                            invalid = True
                            break
                        pos_copy -= 4

                # Check rule #3 - don't move from one spot in the hallway to another in the hallway
                if start_pos >= 16 and pos >= 16: invalid = True

                if not invalid: moves.append((state | amphipod << pos*3, cost))

            neighbors = NEIGHBORS_PART_2[pos]            
        for neighbor in neighbors:
            if state & 0o7 << neighbor*3: continue
            queue.append((neighbor, cost + 10**(amphipod-1)))

    return moves
        
def get_possible_moves(state: int, mode: int) -> list:
    """Get all possible moves for all amphipods at a given state"""
    state_copy = state
    pos = 0
    moves = []
    while state_copy > 0:
        amphipod = state_copy & 0o7
        if amphipod: moves += get_possible_moves_for(state & ~(0o7 << pos*3), pos, amphipod, mode)
        pos += 1
        state_copy >>= 3

    return moves

def get_shortest_path(from_state: int, to_state: int, mode: int) -> int:
    queue = [ (0, from_state) ]
    visited = set()

    while len(queue) > 0:
        energy, state = heapq.heappop(queue)
        if state in visited: continue
        visited.add(state)
        if state == to_state: return energy
        possible_moves = get_possible_moves(state, mode)
        for next_state, next_energy in possible_moves:
            heapq.heappush(queue, (energy + next_energy, next_state))

#
# Puzzle 1 
#
from_state = state_from_string(input_handling.read_from_file('day 23/input.txt'))
to_state = 0o12341234

start_time = time.time()
path = get_shortest_path(from_state, to_state, 1)
print(f'Puzzle 1 solution is: {path} (in {time.time()-start_time:.3f} seconds)')

#
# Puzzle 2
#
from_state = (from_state & 0o77770000) << 24 | 0o43214213 << 12 | from_state & 0o7777
to_state = 0o1234123412341234

start_time = time.time()
path = get_shortest_path(from_state, to_state, 2)
print(f'Puzzle 2 solution is: {path} (in {time.time()-start_time:.3f} seconds)')
