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
    return res


##########
# PART 2 #
##########


def reversible(rng, reverse: bool):
    if reverse:
        return reversed(rng)
    return rng


def cycle(grid):
    load = 0
    for direction in directions():
        load = sum(
            move((i, j), direction, grid)
            for i in reversible(range(grid.shape[0]), direction[0] == 1)
            for j in reversible(range(grid.shape[1]), direction[1] == 1)
            if grid[i,j] == 'O'
        )
    return load


def detect_pattern(seen, current):
    for i, old in enumerate(seen):
        if np.all(old == current):
            return i
    return None


def directions():
    yield NORTH
    yield WEST
    yield SOUTH
    yield EAST


def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    seen = []
    loads = []
    goal = 1_000_000_000 - 1

    for i in range(goal):
        loads.append(cycle(grid))

        if pattern_start := detect_pattern(seen, grid):
            pattern_length = i - pattern_start
            return loads[pattern_start + ((goal - pattern_start) % pattern_length)]
    
        seen.append(np.copy(grid))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
