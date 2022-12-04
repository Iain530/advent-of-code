from utils import read_input, run


FNAME = "04/input.txt"


def parse_line(line):
    return [tuple(map(int, assigned.split('-'))) for assigned in line.strip().split(',')]


##########
# PART 1 #
##########


def is_fully_contained(pair):
    (s1, e1), (s2, e2) = pair
    return s1 >= s2 and e1 <= e2 or s2 >= s1 and e2 <= e1


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    return len(list(filter(is_fully_contained, data)))



##########
# PART 2 #
##########


def is_overlapping(pair):
    (_, e1), (s2, _) = sorted(pair, key=lambda p: p[0])
    return e1 >= s2


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    return len(list(filter(is_overlapping, data)))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
