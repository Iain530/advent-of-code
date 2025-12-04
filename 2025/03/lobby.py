from utils import read_input, run


FNAME = "03/input.txt"


def parse_line(line: str) -> list[int]:
    return [int(c) for c in line]

##########
# PART 1 #
##########


def max_joltage(bank: list[int]) -> int:
    first = max(bank[:-1])
    first_i = bank.index(first)
    second = max(bank[first_i+1:])
    return int(str(first) + str(second))


def part_one(input_file):
    banks = read_input(input_file, parse_chunk=parse_line)
    return sum(max_joltage(bank) for bank in banks)


##########
# PART 2 #
##########

def max_joltage_part_2(bank: list[int], remaining=11) -> str:
    if remaining == 0:
        return str(max(bank))
    
    first = max(bank[:-remaining])
    first_i = bank.index(first)
    
    return str(first) + max_joltage_part_2(bank[first_i+1:], remaining-1)


def part_two(input_file):
    banks = read_input(input_file, parse_chunk=parse_line)
    return sum(int(max_joltage_part_2(bank)) for bank in banks)



if __name__ == '__main__':
    run(part_one, part_two, FNAME)
