import sys, os
sys.path.append(os.getcwd())
from aoc_utils import input_handling

#
# Helper functions
#
def get_element_score(counts: dict, template: str) -> int:
    elements = set(''.join(counts.keys()))
    element_count = {e: 0 for e in elements}
    for k, v in counts.items():
        element_count[k[0]] += v
        element_count[k[1]] += v
    # Every element in a pair appears twice, except for first and last in template - 
    # to be taken into account in calculation of result
    element_count[template[0]] += 1
    element_count[template[-1]] += 1
    return (max(element_count.values()) - min(element_count.values())) // 2

#
# Process input
#
template, insertion_rule_text = input_handling.read_from_file('day 14/input.txt', lambda x: x.split('\n\n'))
insertion_rules = list(map(lambda x: x.split(' -> '), insertion_rule_text.splitlines()))

#
# Puzzle 1 and 2
#
transformations = {}
for input, inject in insertion_rules:
    transformations[input] = (input[0]+inject, inject+input[1])

pairs = {template[i]+template[i+1] for i in range(len(template)-1)}
counts = {p: template.count(p) for p in pairs}

for i in range(40):
    new_counts = {}
    for chars, num in counts.items():
        new_chars1, new_chars2 = transformations[chars]
        new_counts.setdefault(new_chars1, 0)
        new_counts.setdefault(new_chars2, 0)
        new_counts[new_chars1] += num
        new_counts[new_chars2] += num
    counts = new_counts
    if i == 10-1: print(f'Puzzle 1 solution is: {get_element_score(counts, template)}')

print(f'Puzzle 2 solution is: {get_element_score(counts, template)}')
