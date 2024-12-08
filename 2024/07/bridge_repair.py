from utils import read_input, run
from operator import add, mul


FNAME = "07/input.txt"


def parse_line(line: str) -> tuple[int, list[int]]:
    split_line = line.split()
    return int(split_line[0].rstrip(':')), list(map(int, split_line[1:]))
    


##########
# PART 1 #
##########

OPS = [add, mul]


def can_be_true(target: int, remaining: list[int], total: int = 0, ops = OPS) -> bool:
    if total > target:
        return False

    if not remaining:
        return target == total

    return any(can_be_true(target, remaining[1:], op(total, remaining[0]), ops) for op in ops)


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    return sum(target for target, values in data if can_be_true(target, values))


##########
# PART 2 #
##########


def concatenate(a: int, b: int) -> int:
    return int(str(a) + str(b))


NEW_OPS = [concatenate, add, mul]


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    return sum(target for target, values in data if can_be_true(target, values, 0, NEW_OPS))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
