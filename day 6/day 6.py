import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling

#
# Process input
#
fishes = input_handling.read_from_file('day 6/input.txt', lambda x: list(map(int, x.split(','))))

# Consolidate into tuples of counts (timer, number)
fish_counts = []
for i in range(9): fish_counts.append((i, sum(1 for x in fishes if x==i)))

#
# Puzzle 1 & 2
#
for t in range(256):
    for i in range(len(fish_counts)):
        timer, count = fish_counts[i]
        timer -= 1
        if timer < 0:
            timer = 6
            fish_counts.append((8, count))
        fish_counts[i] = (timer, count)

    # Consolidate tuples of counts that are duplicated as a result of fish births
    new_fish_counts = []
    for i in range(9): new_fish_counts.append((i, sum(count for timer, count in fish_counts if timer == i)))
    fish_counts = new_fish_counts
    
    if t == 80-1: p1_solution = sum(count for _, count in fish_counts)

print(f'Puzzle 1 solution is: {p1_solution}')
print(f'Puzzle 2 solution is: {sum(count for _, count in fish_counts)}')