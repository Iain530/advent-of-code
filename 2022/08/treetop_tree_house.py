import numpy as np
import operator as op
from utils import read_input, run
from functools import reduce


FNAME = "08/input.txt"

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)
ALL_DIRECTIONS = (NORTH, EAST, SOUTH, WEST)


##########
# PART 1 #
##########


def get_line_of_sight(grid, coord, direction):
    x, y = coord
    if direction == NORTH:
        return np.flip(grid[:x, y])
    elif direction == EAST:
        return grid[x, y+1:]
    elif direction == SOUTH:
        return grid[x+1:, y]
    elif direction == WEST:
        return np.flip(grid[x, :y])


def is_visible_from_direction(grid, coord, direction):
    blocking_trees = get_line_of_sight(grid, coord, direction)
    return np.all(blocking_trees < grid[coord])


def is_visible(grid, coord):
    return any(is_visible_from_direction(grid, coord, dir) for dir in ALL_DIRECTIONS)


def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=lambda l: list(map(int, l))))
    x_max, y_max = grid.shape
    return sum(is_visible(grid, (x, y)) for x in range(x_max) for y in range(y_max))


##########
# PART 2 #
##########


def find_viewing_distance(grid, coord, direction):
    trees = get_line_of_sight(grid, coord, direction)
    return next((i+1 for i, tree in enumerate(trees) if tree >= grid[coord]), len(trees))


def calculate_scenic_score(grid, coord):
    viewing_distances = [find_viewing_distance(grid, coord, dir) for dir in ALL_DIRECTIONS]
    return reduce(op.mul, viewing_distances, 1)


def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=lambda l: list(map(int, l))))
    x_max, y_max = grid.shape
    return max(calculate_scenic_score(grid, (x, y)) for x in range(x_max) for y in range(y_max))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
