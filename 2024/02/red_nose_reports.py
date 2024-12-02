from utils import read_input, run, sliding_window


FNAME = "02/input.txt"


##########
# PART 1 #
##########


def is_safe(report: list[int]) -> bool:
    if report[0] > report[-1]:
        return is_safe(list(reversed(report)))
    return all(1 <= (b - a) <= 3 for a, b in sliding_window(report, 2))


def part_one(input_file):
    data = read_input(input_file, parse_chunk=lambda l: list(map(int, l.split())))
    return sum(1 if is_safe(report) else 0 for report in data)


##########
# PART 2 #
##########


def copy_without_index(report: list[int], i: int) -> list[int]:
    copy = report.copy()
    copy.pop(i)
    return copy


def is_safe_removed(report: list[int]) -> bool:    
    return is_safe(report) or any(is_safe(copy_without_index(report, i)) for i in range(len(report)))


def part_two(input_file):
    data = read_input(input_file, parse_chunk=lambda l: list(map(int, l.split())))
    return sum(1 if is_safe_removed(report) else 0 for report in data)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
