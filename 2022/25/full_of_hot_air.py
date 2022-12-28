import math
from utils import read_input, run


FNAME = "25/input.txt"


##########
# PART 1 #
##########

bases = [5 ** i for i in range(20)]


KEY = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}
REVERSE_KEY = {v: k for v, k in KEY.items()}


def snafu_to_decimal(snafu):
    return sum((5 ** i) * KEY[s] for i, s in enumerate(reversed(snafu)))


def to_base_5(n):
    res = []
    while n:
        res = [n % 5] + res
        n //= 5
    return res


def decimal_to_snafu(dec):
    base_5 = [0] + to_base_5(dec)
    for i in reversed(range(len(base_5))):
        if base_5[i] == 3:
            base_5[i-1] += 1
            base_5[i] = '='
        elif base_5[i] == 4:
            base_5[i-1] += 1
            base_5[i] = '-'
        else:
            base_5[i] = str(base_5[i])
    return ''.join(base_5).lstrip('0')


def part_one(input_file):
    data = read_input(input_file, parse_chunk=lambda l: l)
    total = sum(snafu_to_decimal(snafu) for snafu in data)
    return decimal_to_snafu(total)


##########
# PART 2 #
##########


def part_two(input_file):
    pass


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
