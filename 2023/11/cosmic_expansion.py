from utils import read_input, run
import numpy as np
from itertools import combinations


FNAME = "11/input.txt"


##########
# PART 1 #
##########


def find_galaxies(grid) -> list[tuple[int, int]]:
    return {
        (i, j)
        for i in range(grid.shape[0])
        for j in range(grid.shape[1])
        if grid[i,j] == '#'
    }


def dist(g1, g2) -> int:
    return sum(abs(a - b) for a, b in zip(g1, g2))


def find_empty_rows_and_cols(grid):
    double_rows = set()
    double_cols = set()
    for i in range(grid.shape[0]):
        if np.all(grid[i,:] == '.'):
            double_rows.add(i)
    for i in range(grid.shape[1]):
        if np.all(grid[:,i] == '.'):
            double_cols.add(i)
    return double_rows, double_cols



def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=lambda l: list(l)))
    double_rows, double_cols = find_empty_rows_and_cols(grid)

    for row in sorted(double_rows, reverse=True):
        grid = np.concatenate((grid[:row + 1], grid[row:]))
    for col in sorted(double_cols, reverse=True):
        grid = np.concatenate((grid[:,:col + 1], grid[:,col:]), axis=1)
    
    return sum(dist(g1, g2) for g1, g2 in combinations(find_galaxies(grid), 2))


##########
# PART 2 #
##########


def count_crossings(g1, g2, empty_rows, empty_cols):
    g1_x, g1_y = g1
    g2_x, g2_y = g2
    cols = sum(1 for row in empty_rows if min(g1_x, g2_x) < row < max(g1_x, g2_x))
    rows = sum(1 for col in empty_cols if min(g1_y, g2_y) < col < max(g1_y, g2_y))
    return cols + rows


def large_dist(g1, g2, empty_rows, empty_cols) -> int:
    return dist(g1, g2) + 999_999 * count_crossings(g1, g2, empty_rows, empty_cols)


def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=lambda l: list(l)))
    empty_rows, empty_cols = find_empty_rows_and_cols(grid)
    return sum(large_dist(g1, g2, empty_rows, empty_cols) for g1, g2 in combinations(find_galaxies(grid), 2))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
