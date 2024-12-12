from utils import read_input, run
import numpy as np
from collections import defaultdict


FNAME = "10/input.txt"
Vector = tuple[int, int]
Grid = np.ndarray

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

def is_in_grid(coord: Vector, grid: Grid) -> bool:
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))


def add(v1: Vector, v2: Vector) -> Vector:
    return tuple(a + b for a, b in zip(v1, v2))


def parse_input(input_file):
    return np.array(read_input(input_file, parse_chunk=lambda l: list(map(int, l))))


##########
# PART 1 #
##########


def neighbours(coord: Vector, grid: Grid):
    return filter(lambda c: is_in_grid(c, grid), (add(coord, d) for d in DIRECTIONS))


def uphill_neighbours(coord: Vector, grid: Grid):
    return (n for n in neighbours(coord, grid) if grid[n] == grid[coord] + 1)


def find_peaks(coord: Vector, grid: Grid, peaks: Grid) -> int:
    if coord in peaks:
        return peaks[coord]
    
    if grid[coord] == 9:
        peaks[coord].add(coord)
        return peaks[coord]
    
    for n in uphill_neighbours(coord, grid):
        peaks[coord] |= find_peaks(n, grid, peaks)
    
    return peaks[coord]


def part_one(input_file):
    grid = parse_input(input_file)
    peaks = defaultdict(set)

    total = 0

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[(i, j)] == 0:
                total += len(find_peaks((i, j), grid, peaks))
    
    return total


##########
# PART 2 #
##########


def calculate_score(coord: Vector, grid: Grid, scores: Grid) -> int:
    if scores[coord] != -1:
        return scores[coord]
    
    if grid[coord] == 9:
        scores[coord] = 1
        return 1
    
    scores[coord] = sum(calculate_score(n, grid, scores) for n in uphill_neighbours(coord, grid))
    return scores[coord]


def part_two(input_file):
    grid = parse_input(input_file)
    scores = np.zeros(grid.shape, dtype=np.int32)
    scores.fill(-1)

    total = 0

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[(i, j)] == 0:
                total += calculate_score((i, j), grid, scores)
    return total


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
