from utils import read_input, run
from operator import add, mul
from functools import reduce


FNAME = "06/input.txt"


def parse_line(line: str) -> list[int]:
    if '+' in line:
        return line.split()

    return list(map(int, line.split()))

##########
# PART 1 #
##########

OPS = {
    '*': mul,
    '+': add,
}


def part_one(input_file):
    problems = read_input(input_file, parse_chunk=parse_line)
    total = 0
    for i in range(len(problems[0])):
        operator = OPS[problems[-1][i]]
        numbers = [problems[j][i] for j in range(len(problems) - 1)]
        total += reduce(operator, numbers)
    
    return total


##########
# PART 2 #
##########


def parse_column(problems: list[list[str]], col: int) -> int:
    rows = len(problems) - 1
    return ''.join(problems[i][col] for i in range(rows)).strip()


def part_two(input_file):
    problems = read_input(input_file, parse_chunk=str)
    numbers = []
    total = 0

    for col in reversed(range(len(problems[0]))):
        num = parse_column(problems, col)
        if not num:
            numbers = []
            continue

        numbers.append(int(num))

        if col < len(problems[-1]) and (operator := problems[-1][col]) != ' ':
            total += reduce(OPS[operator], numbers)
        
    return total


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
