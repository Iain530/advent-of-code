from utils import read_input, run
from itertools import cycle
import math


FNAME = "08/input.txt"


def parse_chunk(para: str):
    if '=' not in para:
        return [0 if i == 'L' else 1 for i in para.strip()]

    nodes = {}
    for line in para.split('\n'):
        source, destination = line.split(' = ')
        left, right = destination.strip('()').split(', ')
        nodes[source] = (left, right)
    return nodes


##########
# PART 1 #
##########


def part_one(input_file):
    directions, nodes = read_input(input_file, parse_chunk=parse_chunk, separator='\n\n')
    current = 'AAA'
    return next(i + 1 for i, d in enumerate(cycle(directions)) if (current := nodes[current][d]) == 'ZZZ')


##########
# PART 2 #
##########


def count_steps_to_end(start, directions, nodes):
    current = start
    return next(i + 1 for i, d in enumerate(cycle(directions)) if (current := nodes[current][d]).endswith('Z'))


def part_two(input_file):
    directions, nodes = read_input(input_file, parse_chunk=parse_chunk, separator='\n\n')
    return math.lcm(*(count_steps_to_end(s, directions, nodes) for s in nodes if s.endswith('A')))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
