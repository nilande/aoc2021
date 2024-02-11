import sys, os
sys.path.append(os.getcwd())
from aoc_utils.input_handling import read_lines_from_file

#
# Process input
#
bit_strings = read_lines_from_file('day 3/input.txt')

#
# Puzzle 1
#
numbers = len(bit_strings)
bit_length = len(bit_strings[0])
bit_counts = []
for i in range(bit_length): bit_counts.append(sum(x[i] == '1' for x in bit_strings))

gamma_rate = 0
for i in range(bit_length):
    gamma_rate <<= 1
    if bit_counts[i] > numbers//2: gamma_rate |= 1
epsilon_rate = 2**bit_length-1 - gamma_rate

print(f'Puzzle 1 solution is: {gamma_rate * epsilon_rate}')

#
# Puzzle 2
#
o_str = bit_strings.copy()
for i in range(bit_length):
    ones = sum(x[i] == '1' for x in o_str)
    if ones * 2 >= len(o_str):
        o_str = [x for x in o_str if x[i] == '1']
    else:
        o_str = [x for x in o_str if x[i] == '0']
    if len(o_str) == 1: break
oxygen_rating = 0
for c in o_str[0]:
    oxygen_rating <<= 1
    if c == '1': oxygen_rating |= 1

co2_str = bit_strings.copy()
for i in range(bit_length):
    zeros = sum(x[i] == '0' for x in co2_str)
    if zeros * 2 <= len(co2_str):
        co2_str = [x for x in co2_str if x[i] == '0']
    else:
        co2_str = [x for x in co2_str if x[i] == '1']
    if len(co2_str) == 1: break
co2_scrubber_rating = 0
for c in co2_str[0]:
    co2_scrubber_rating <<= 1
    if c == '1': co2_scrubber_rating |= 1

print(f'Puzzle 2 solution is: {oxygen_rating * co2_scrubber_rating}')