from utils import read_input, run
from itertools import chain
from functools import cache


FNAME = "11/input.txt"


##########
# PART 1 #
##########


def blink(stone: int) -> tuple[int]:
    if stone == 0:
        return (1,)
    
    if (length := len(str(stone))) % 2 == 0:
        return int(str(stone)[:(length//2)]), int(str(stone)[(length//2):])
    
    return (stone * 2024,)


def blink_all(stones: list[int]) -> list[int]:
    return list(chain.from_iterable(map(blink, stones)))


def part_one(input_file):
    stones = read_input(input_file, parse_chunk=lambda l: list(map(int, l.split())))[0]

    for _ in range(25):
        stones = blink_all(stones)

    return len(stones)

##########
# PART 2 #
##########


@cache
def count_stones(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1

    if stone == 0:
        return count_stones(1, blinks - 1)
    
    if (length := len(str(stone))) % 2 == 0:
        left = int(str(stone)[:(length//2)])
        right = int(str(stone)[(length//2):])
        return count_stones(left, blinks - 1) + count_stones(right, blinks - 1)
    
    return count_stones(stone * 2024, blinks - 1)


def part_two(input_file):
    stones = read_input(input_file, parse_chunk=lambda l: list(map(int, l.split())))[0]

    return sum(count_stones(stone, blinks=75) for stone in stones)
        

if __name__ == '__main__':
    run(part_one, part_two, FNAME)
