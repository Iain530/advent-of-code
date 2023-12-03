from utils import read_input, run
import numpy as np
from typing import Iterable
from collections import defaultdict

Coord = tuple[int, int]

FNAME = "03/input.txt"


##########
# PART 1 #
##########

def get_adjacent_coords(number_coords: list[Coord]):
    adj = set()
    for x, y in number_coords:
        adj |= {
            (x - 1, y -1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y -1),
            (x + 1, y),
            (x + 1, y + 1),
        }
    return adj - set(number_coords)


def is_in_grid(coord, grid):
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))


def get_grid_values(coords: Iterable[Coord], grid):
    return (grid[c] for c in coords if is_in_grid(c, grid))


def is_part_number(number: list[Coord], grid):
    return any(
        char != '.' and not char.isnumeric()
        for char in get_grid_values(get_adjacent_coords(number), grid)
    )


def find_number(first_numeric_coord: Coord, grid):
    number = [first_numeric_coord]
    x, y = first_numeric_coord
    next_coord = (x, y + 1)
    while is_in_grid(next_coord, grid) and grid[next_coord].isnumeric():
        number.append(next_coord)
        next_coord = (x, next_coord[1] + 1)
    return number


def number_coords_to_int(number: list[Coord], grid):
    return int(''.join(get_grid_values(number, grid)))


def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))

    i = 0
    total = 0
    while i < grid.shape[0]:
        j = 0
        while j < grid.shape[1]:
            coord = (i, j)
            if grid[coord].isnumeric():
                number = find_number(coord, grid)
                if is_part_number(number, grid):
                    total += number_coords_to_int(number, grid)
                j = number[-1][1]
            j += 1
        i += 1

    return total


##########
# PART 2 #
##########


def record_gears(gears: dict[Coord, list[int]], number: list[Coord], grid):
    adj = get_adjacent_coords(number)
    for coord in adj:
        if is_in_grid(coord, grid) and grid[coord] == '*':
            gears[coord].append(number_coords_to_int(number, grid))



def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))

    gears = defaultdict(list)
    i = 0
    while i < grid.shape[0]:
        j = 0
        while j < grid.shape[1]:
            coord = (i, j)
            if grid[coord].isnumeric():
                number = find_number(coord, grid)
                record_gears(gears, number, grid)
                j = number[-1][1]
            j += 1
        i += 1
    return sum(gear[0] * gear[1] for gear in gears.values() if len(gear) == 2)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
