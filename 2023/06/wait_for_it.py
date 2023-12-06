from utils import read_input, run
from functools import reduce
from operator import mul


FNAME = "06/input.txt"


def parse_line(line: str):
    return list(map(int, line.split(':')[1].strip().split()))


##########
# PART 1 #
##########


def find_margin(race):
    time, distance = race
    min_time = next(t for t in range(time) if t * (time - t) >= distance)
    return time - (min_time * 2) + 1


def part_one(input_file):
    time, distance = read_input(input_file, parse_chunk=parse_line)
    races = list(zip(time, distance))
    return reduce(mul, map(find_margin, races), 1)


##########
# PART 2 #
##########


def parse_line_as_one(line: str):
    return int(''.join(line.split(':')[1].strip().split()))


def part_two(input_file):
    time, distance = read_input(input_file, parse_chunk=parse_line_as_one)
    print(time, distance)
    return find_margin((time, distance))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
