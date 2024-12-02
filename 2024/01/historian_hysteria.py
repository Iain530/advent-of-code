from utils import read_input, run
from collections import Counter


FNAME = "01/input.txt"


def parse_input(input_file):
    data = read_input(input_file, parse_chunk=lambda l: list(map(int, l.split())))
    list_a = [l[0] for l in data]
    list_b = [l[1] for l in data]
    return list_a, list_b


##########
# PART 1 #
##########


def part_one(input_file):
    list_a, list_b = parse_input(input_file)
    return sum(abs(a - b) for a, b in zip(sorted(list_a), sorted(list_b)))


##########
# PART 2 #
##########


def part_two(input_file):
    list_a, list_b = parse_input(input_file)
    b_counts = Counter(list_b)
    return sum(a * b_counts[a] for a in list_a)




if __name__ == '__main__':
    run(part_one, part_two, FNAME)
