from utils import read_input, run
from collections import defaultdict


FNAME = "04/input.txt"


def parse_chunk(line: str):
    winning, numbers = line.split(': ')[1].split(' | ')
    winning_set =  {int(w) for w in winning.strip().split()}
    my_numbers = [int(n) for n in numbers.strip().split()]
    return winning_set, my_numbers


##########
# PART 1 #
##########

def score(winning_set, numbers):
    matches = sum(1 for n in numbers if n in winning_set)
    return 2 ** (matches - 1) if matches > 0 else 0


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_chunk)
    return sum(score(winning_set, numbers) for winning_set, numbers in data)


##########
# PART 2 #
##########


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_chunk)

    copies = defaultdict(lambda: 1)
    total = 0
    for card_id, (winning_set, numbers) in enumerate(data):
        total += copies[card_id]
        matches = sum(1 for n in numbers if n in winning_set)
        for i in range(matches):
            copies[card_id + 1 + i] += 1 * copies[card_id]

    return total


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
