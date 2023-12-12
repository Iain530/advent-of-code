from utils import read_input, run
from functools import cache


FNAME = "12/input.txt"


def parse_line(line: str) -> tuple[str, list[int]]:
    springs, rest = line.split()
    return springs, tuple(int(d) for d in rest.split(','))



##########
# PART 1 #
##########


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    return sum(count(spring, conditions, 0) for spring, conditions in data)


##########
# PART 2 #
##########

@cache
def count(springs: str, conditions: tuple[int], current_group_size: int) -> int:
    # print(springs, conditions, current_group_size)

    if not conditions:
        return '#' not in springs
    if conditions and not springs:
        if len(conditions) == 1 and current_group_size == conditions[0]:
            return 1
        return 0

    next_condition = conditions[0]
    remaining_conditions = conditions[1:]
    next_char = springs[0]
    remaining_springs = springs[1:]

    if next_char == '.':
        if current_group_size == 0:
            return count(remaining_springs, conditions, 0)

        if current_group_size == next_condition:
            return count(remaining_springs, remaining_conditions, 0)
        return 0

    if next_char == '#':
        if current_group_size < next_condition:
            return count(remaining_springs, conditions, current_group_size + 1)
        return 0

    if next_char == '?':
        if current_group_size == 0:
            return (
                count(remaining_springs, conditions, 1)
                + count(remaining_springs, conditions, 0)
            )
        
        if current_group_size < next_condition:
            return count(remaining_springs, conditions, current_group_size + 1)
        
        if current_group_size == next_condition:
            return count(remaining_springs, remaining_conditions, 0)
        
        return 0    


def unfold_line(line: str) -> tuple[str, list[int]]:
    springs, conditions = parse_line(line)
    return '?'.join([springs] * 5), conditions * 5


def part_two(input_file):
    data = read_input(input_file, parse_chunk=unfold_line)
    return sum(count(spring.lstrip('.'), conditions, 0) for spring, conditions in data)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)