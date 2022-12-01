from utils import read_input, run


fname = "01/input.txt"


def parse_chunk(chunk):
    return list(map(int, chunk.strip().split('\n')))

##########
# PART 1 #
##########


def part_one():
    data = read_input(fname, separator='\n\n', parse_chunk=parse_chunk)
    return sum(max(data, key=sum))


##########
# PART 2 #
##########


def part_two():
    data = read_input(fname, separator='\n\n', parse_chunk=parse_chunk)
    top_three = sorted(data, key=sum)[-3:]
    return sum(map(sum, top_three))


if __name__ == '__main__':
    run(part_one, part_two)
