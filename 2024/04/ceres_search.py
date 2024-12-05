from utils import read_input, run
import numpy as np


FNAME = "04/input.txt"
Vector = tuple[int, int]
Grid = np.ndarray


##########
# PART 1 #
##########


UP = (-1, 0)
UP_LEFT = (-1, -1)
LEFT = (0, -1)
DOWN_LEFT = (1, -1)
DOWN = (1, 0)
DOWN_RIGHT = (1, 1)
RIGHT = (0, 1)
UP_RIGHT = (-1, 1)

DIRECTIONS = [UP, UP_LEFT, LEFT, DOWN_LEFT, DOWN, DOWN_RIGHT, RIGHT, UP_RIGHT]

def is_in_grid(coord: Vector, grid: Grid) -> bool:
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))


def add(v1: Vector, v2: Vector) -> Vector:
    return tuple(a + b for a, b in zip(v1, v2))


def mul(v: Vector, scale: int) -> Vector:
    return tuple(a * scale for a in v)


def word(coord: Vector, direction: Vector, start=0, end=4):
    return [add(coord, mul(direction, i)) for i in range(start, end)]


def is_word_in_grid(word: list[Vector], grid):
    return all(is_in_grid(coord, grid) for coord in word)


def all_directions(coord: Vector, grid) -> list[list[Vector]]: 
    return [w for w in (word(coord, direction) for direction in DIRECTIONS) if is_word_in_grid(w, grid)]


def is_xmas(word: list[Vector], grid, expected='XMAS') -> bool:
    return ''.join(grid[c] for c in word) == expected


def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    xmas = 0
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[(i, j)] == 'X':
                xmas += sum(1 if is_xmas(word, grid) else 0 for word in all_directions((i, j), grid))
    return xmas

##########
# PART 2 #
##########


DIAGONALS = [UP_LEFT, DOWN_LEFT, UP_RIGHT, DOWN_RIGHT]

def diagonal_directions(coord, grid):
    return [w for w in (word(coord, direction, start=-1, end=2) for direction in DIAGONALS) if is_word_in_grid(w, grid)]


def is_x(words: list[list[Vector]], grid) -> bool:
    return sum(1 if is_xmas(w, grid, 'MAS') else 0 for w in words) == 2


def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    xmas = 0
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[(i, j)] == 'A':
                xmas += 1 if is_x(diagonal_directions((i, j), grid), grid) else 0
    return xmas


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
