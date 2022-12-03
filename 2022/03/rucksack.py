from utils import read_input, run, run_test


FNAME = "03/input.txt"

def priority(letter):
    if letter.isupper():
        return ord(letter) - 38
    return ord(letter) - 96


def parse_line(line) -> tuple[set[int], set[int]]:
    priorities = list(map(priority, line))
    size = len(priorities)
    return set(priorities[:size//2]), set(priorities[size//2:])


##########
# PART 1 #
##########


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    # print(data)
    return sum(sum(c1.intersection(c2)) for c1, c2 in data)


##########
# PART 2 #
##########


def group_elves(data, group_size=3):
    return [data[i:i+group_size] for i in range(0, len(data), group_size)]


def part_two(input_file):
    data = group_elves(read_input(input_file, parse_chunk=lambda l: set(map(priority, l))))
    return sum(sum(set.intersection(*group)) for group in data)



if __name__ == '__main__':
    run_test(part_one, "03/test_input.txt", 0, "test priorities", exit_on_fail=True)
    run(part_one, part_two, FNAME)
