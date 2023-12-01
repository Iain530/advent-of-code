from utils import read_input, run


FNAME = "01/input.txt"


##########
# PART 1 #
##########


def part_one(input_file):
    data = read_input(input_file, parse_chunk=lambda l: ''.join(c for c in l if c.isnumeric()))
    return sum(int(l[0] + l[-1]) for l in data)


##########
# PART 2 #
##########

digits_map = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def find_first_number(line: str):
    if line[0].isnumeric():
        return line[0]

    for alpha, numeric in digits_map.items():
        if line.startswith(alpha):
            return numeric

    return find_first_number(line[1:])


def find_last_number(line: str):
    if line[-1].isnumeric():
        return line[-1]

    for alpha, numeric in digits_map.items():
        if line.endswith(alpha):
            return numeric

    return find_last_number(line[:-1])
        
            

def part_two(input_file):
    data = read_input(input_file, parse_chunk=str)
    return sum(int(find_first_number(l) + find_last_number(l)) for l in data)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
