from utils import read_input, run, iter_grid, add, is_in_grid
import numpy as np


FNAME = "04/input.txt"


##########
# PART 1 #
##########


def is_reachable(grid, point) -> bool:
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            adj_point = add(point, (i, j))

            if adj_point == point or not is_in_grid(adj_point, grid):
                continue

            if grid[adj_point] == '@':
                count += 1
    return count < 4


def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))

    return sum(int(is_reachable(grid, point)) for point in iter_grid(grid) if grid[point] == '@')


##########
# PART 2 #
##########

def find_removable(grid):
    return [point for point in iter_grid(grid) if grid[point] == '@' and is_reachable(grid, point)]


def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    removed = 0
    removable = find_removable(grid)
    
    while len(removable):
        for point in removable:
            grid[point] = 'x'
        removed += len(removable)

        removable = find_removable(grid)
    
    return removed


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
