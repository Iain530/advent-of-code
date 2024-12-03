from utils import read_input, run
import re
from typing import Iterator


FNAME = "03/input.txt"


##########
# PART 1 #
##########


def parse_mul(raw_mul: str) -> tuple[int, int]:
    return tuple(map(int, raw_mul.strip('mul()').split(',')))


def part_one(input_file):
    data = '\n'.join(read_input(input_file, parse_chunk=str))
    return sum(a * b for a, b in map(parse_mul, re.findall('mul\(\d+,\d+\)', data)))


##########
# PART 2 #
##########


def part_two(input_file):
    data = '\n'.join(read_input(input_file, parse_chunk=str))
    do = '\n'.join(l.split("don't()")[0] for l in data.split('do()'))
    return sum(a * b for a, b in map(parse_mul, re.findall('mul\(\d+,\d+\)', do)))

if __name__ == '__main__':
    run(part_one, part_two, FNAME)
