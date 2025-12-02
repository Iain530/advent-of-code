from utils import read_input, run


FNAME = "02/input.txt"


def parse_line(line: str):
    return [id_range.split('-') for id_range in line.split(',')]


##########
# PART 1 #
##########


def is_invalid(number: str) -> bool:
    id = str(number)

    if len(id) % 2 != 0:
        return False

    half = len(id) // 2
    prefix = id[:half]
    return id == prefix * 2


def part_one(input_file):
    ranges = read_input(input_file, parse_chunk=parse_line)[0]

    total = 0
    for (low, high) in ranges:
        for number in range(int(low), int(high) + 1):
            if has_repeated_pattern(number):
                total += number

    return total



##########
# PART 2 #
##########


def has_repeated_pattern(number: int, length=2) -> bool:
    id = str(number)

    if len(id) % length != 0:
        return False

    split = len(id) // length
    prefix = id[:split]
    return id == prefix * length


def is_invalid_part_2(number: int) -> bool:
    return any(has_repeated_pattern(number, length) for length in range(2, len(str(number)) + 1))


def part_two(input_file):
    ranges = read_input(input_file, parse_chunk=parse_line)[0]

    total = 0
    for (low, high) in ranges:
        for number in range(int(low), int(high) + 1):
            if is_invalid_part_2(number):
                total += number

    return total



if __name__ == '__main__':
    run(part_one, part_two, FNAME)
