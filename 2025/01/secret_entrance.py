from utils import read_input, run


FNAME = "01/input.txt"

def parse_line(line: str) -> tuple[str, int]:
    return line[0], int(line[1:])


##########
# PART 1 #
##########

SCALE = {
    'L': -1,
    'R': 1,
}


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    value = 50
    count = 0
    for direction, distance in data:
        value += distance * SCALE[direction]
        if value % 100 == 0:
            count += 1
    return count


##########
# PART 2 #
##########



def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    value = 50
    count = 0
    for direction, distance in data:
        next_value = value + (distance * SCALE[direction])
        
        count += abs(next_value // 100)
        if value == 0 and next_value < 0:
            count -= 1
        if next_value <= 0 and next_value % 100 == 0:
            count += 1

        value = next_value % 100

    return count


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
