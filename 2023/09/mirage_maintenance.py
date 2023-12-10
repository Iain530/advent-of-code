from utils import read_input, run, sliding_window


FNAME = "09/input.txt"


def parse_line(line: str) -> list[int]:
    return list(map(int, line.split()))


##########
# PART 1 #
##########


def diff_sequence(seq: list[int]) -> list[int]:
    return [b - a for a, b in sliding_window(seq, 2)]


def find_next_value(seq: list[int]) -> int:
    seqs = [seq]
    while not all(s == 0 for s in seqs[-1]):
        seqs.append(diff_sequence(seqs[-1]))
    return sum(s[-1] for s in seqs)


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    return sum(find_next_value(seq) for seq in data)


##########
# PART 2 #
##########


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    return sum(find_next_value(seq[::-1]) for seq in data)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
