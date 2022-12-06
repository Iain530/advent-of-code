from utils import read_input, run


FNAME = "06/input.txt"


##########
# PART 1 #
##########


def part_one(input_file):
    data = read_input(input_file)[0][0]
    for i in range(len(data) - 4):
        if len(set(data[i:i+4])) == 4:
            return i+4


##########
# PART 2 #
##########


def part_two(input_file):
    data = read_input(input_file)[0][0]
    for i in range(len(data) - 14):
        if len(set(data[i:i+14])) == 14:
            return i+14


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
