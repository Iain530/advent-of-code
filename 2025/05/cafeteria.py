from utils import read_input, run


FNAME = "05/input.txt"


def parse_input(input_file):
    ranges_raw, ingredients = read_input(input_file, separator='\n\n')
    
    ranges = [tuple(map(int, rng.split('-'))) for rng in ranges_raw]
    return ranges, list(map(int, ingredients))


##########
# PART 1 #
##########


def is_fresh(ingredient: int, ranges: list[tuple[int, int]]) -> bool:
    return any(low <= ingredient <= high for low, high in ranges)


def part_one(input_file):
    ranges, ingredients = parse_input(input_file)
    return sum(1 for ingredient in ingredients if is_fresh(ingredient, ranges))


##########
# PART 2 #
##########


def part_two(input_file):
    ranges, _ = parse_input(input_file)    

    pointer = -1
    fresh_ids = 0

    for rang in sorted(ranges, key=lambda r: r[0]):
        if pointer < rang[0]:
            pointer = rang[0]
            fresh_ids += 1

        if pointer >= rang[1]:
            continue

        fresh_ids += rang[1] - pointer
        pointer = rang[1]
    
    return fresh_ids


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
