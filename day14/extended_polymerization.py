from utils import read_input, timed
from day1.sonar2 import sliding_window
from itertools import chain
from collections import Counter
from functools import cache


fname = "day14/input.txt"


def parse(fname):
    lines = list(read_input(fname)) 
    template = lines[0][0]
    rules = {tuple(rule[0]): rule[2] for rule in lines[2:]}
    return template, rules


##########
# PART 1 #
##########

def step(template, rules):
    new = [rules[pair] for pair in sliding_window(template, 2)]
    return ''.join(chain(*zip(template, new))) + template[-1]
        


def part_one():
    template, rules = parse(fname)
    for _ in range(10):
        template = step(template, rules)
    
    counter = Counter(template)
    most_common, *_, least_common = counter.most_common()

    return most_common[1] - least_common[1]


##########
# PART 2 #
##########


def make_traverse(rules, target_depth):

    @cache
    def traverse(template, depth=0):
        if depth == target_depth:
            return Counter(template[1:]) # Ignore first char as it overlaps previous chunk
        
        counts = Counter()
        for pair in pairs(template):
            new = rules[pair]
            counts.update(traverse(pair[0] + new + pair[1], depth + 1))
        
        return counts
    
    return traverse
    

def pairs(template):
    return (pair for pair in sliding_window(template, 2))


def part_two():
    template, rules = parse(fname)
    
    traverse = make_traverse(rules, target_depth=40)
    counts = traverse(template)
    counts[template[0]] += 1 # Make up for missing first char of chunk 1

    most_common, *_, least_common = counts.most_common()
    return most_common[1] - least_common[1]


if __name__ == '__main__':
    print("PART 1")
    result, time = timed(part_one)
    print(f"Answer:\t{result}\nTime:\t{time*1000}ms")
    print()
    print(f"PART 2")
    result, time = timed(part_two)
    print(f"Answer:\t{result}\nTime:\t{time*1000}ms")
