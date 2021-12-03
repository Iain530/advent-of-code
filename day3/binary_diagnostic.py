from utils import read_input
from collections import Counter


def transpose(matrix):
    return list(zip(*matrix))


def binary_bools_to_int(bools) -> int:
    return int(''.join('01'[b] for b in bools), 2)


def part_one():
    numbers = [[bool(int(digit)) for digit in bin_string] for bin_string in read_input('day3/input.txt', types=[str])]
    per_digit = transpose(numbers)

    counts = [Counter(digits) for digits in per_digit]

    gamma_values = [count.most_common(1)[0][0] for count in counts]
    epsilon_values = [not g for g in gamma_values]

    gamma = binary_bools_to_int(gamma_values)
    epsilon = binary_bools_to_int(epsilon_values)

    print(gamma * epsilon)


##########
# PART 2 #
##########


def digits_at_index(numbers, i):
    return (number[i] for number in numbers)


def find_rating(numbers, filter_for_most_common: bool):
    i = 0
    possible = numbers
    while len(possible) > 1:
        counts = Counter(digits_at_index(possible, i))
        most_common = counts[True] >= counts[False]
        filter_value = most_common if filter_for_most_common else not most_common
        possible = [p for p in possible if p[i] is filter_value]
        i += 1

    if len(possible) == 1:
        result = binary_bools_to_int(possible[0])
        return result
    else:
        print(f'Unable to find a single number, remaining={possible}')
        exit(1)


def part_two():
    numbers = [[bool(int(digit)) for digit in bin_string] for bin_string in read_input('day3/input.txt', types=[str])]

    oxygen_rating = find_rating(numbers, filter_for_most_common=True)
    co2_rating = find_rating(numbers, filter_for_most_common=False)

    print(oxygen_rating * co2_rating)


if __name__ == '__main__':
    part_two()
