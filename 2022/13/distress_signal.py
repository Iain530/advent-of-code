from utils import read_input, run
from functools import cmp_to_key
import json


FNAME = "13/input.txt"

##########
# PART 1 #
##########


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        return left - right
    
    if isinstance(left, list) and isinstance(right, list):
        for left_v, right_v in zip(left, right):
            if (result := compare(left_v, right_v)) != 0:
                return result
        
        if len(left) == len(right):
            return 0
        return len(left) - len(right)
    
    if isinstance(left, int):
        return compare([left], right)
    
    if isinstance(right, int):
        return compare(left, [right])


def part_one(input_file):
    data = read_input(input_file, separator='\n\n', parse_chunk=lambda c: tuple(map(json.loads, c.split('\n'))))
    return sum(i+1 for i, diff in enumerate(compare(l, r) for l, r in data) if diff < 0)


##########
# PART 2 #
##########


def part_two(input_file):
    data = list(filter(lambda x: x is not None, read_input(input_file, separator='\n', parse_chunk=lambda c: json.loads(c) if c else None)))
    data += [[[2]], [[6]]]
    sorted_data = sorted(data, key=cmp_to_key(compare))
    return (sorted_data.index([[2]]) + 1) * (sorted_data.index([[6]]) + 1)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
