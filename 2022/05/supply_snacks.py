from utils import run
from collections import deque


FNAME = "05/input.txt"


def read_input(fname):
    with open(fname, 'r') as f:
        raw_crates, raw_steps = f.read().strip().split('\n\n')
    
    *raw_crates, crate_numbers = raw_crates.splitlines()
    
    crate_indexes = {int(num): i for i, num in enumerate(crate_numbers) if num.isnumeric()}
    stacks = [deque() for i in range(len(crate_indexes))]

    for row in raw_crates[::-1]:
        for stack_no, position in crate_indexes.items():
            if (crate := row[position]).isupper():
                stacks[stack_no - 1].append(crate)

    moves = [tuple(int(word) for word in line.split(' ') if word.isnumeric()) for line in raw_steps.splitlines()]
    return stacks, moves


##########
# PART 1 #
##########


def part_one(input_file):
    stacks, moves = read_input(input_file)

    for count, origin, target in moves:
        for _ in range(count):
            stacks[target - 1].append(stacks[origin - 1].pop())
    
    return ''.join(s[-1] for s in stacks)


##########
# PART 2 #
##########


def part_two(input_file):
    stacks, moves = read_input(input_file)

    for count, origin, target in moves:
        moving = deque()
        for _ in range(count):
            moving.appendleft(stacks[origin - 1].pop())
        stacks[target - 1].extend(moving)
    
    return ''.join(s[-1] for s in stacks)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
