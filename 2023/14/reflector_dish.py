from utils import read_input, run
import numpy as np


FNAME = "14/input.txt"


##########
# PART 1 #
##########

Vector = tuple[int, int]
Grid = np.ndarray

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)


def is_in_grid(coord: Vector, grid: Grid) -> bool:
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))


def add_vector(a: Vector, b: Vector) -> Vector:
    return tuple(v1 + v2 for v1, v2 in zip(a, b))


def can_move(to: Vector, grid: Grid) -> bool:
    return is_in_grid(to, grid) and grid[to] == '.'


def move(start: Vector, direction: Vector, grid: Grid) -> int:
    current = start
    moves = 0
    while can_move(to := add_vector(current, direction), grid):
        grid[to] = grid[current]
        grid[current] = '.'
        current = to
        moves += 1
    # print(f'Moved {start} {moves} NORTH to {current}')
    return grid.shape[0] - current[0]


def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    res = sum(
        move((i, j), NORTH, grid)
        for i in range(grid.shape[0])
        for j in range(grid.shape[1])
        if grid[i,j] == 'O'
    )
    print(grid)
    return res


##########
# PART 2 #
##########


def cycle(grid):
    return sum(
        move((i, j), NORTH, grid)
        for i in range(grid.shape[0])
        for j in range(grid.shape[1])
        if grid[i,j] == 'O'
    )


def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    load = 0
    print(np.rot90(grid))
    for i in range(1_000_000_000):
        if i % 1_000 == 0:
            print(f'{i * 100 / 1_000_000_000}% load: {load}')
        load = cycle(grid)
        grid = np.rot90(grid, axes=(1, 0))
    return load


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
