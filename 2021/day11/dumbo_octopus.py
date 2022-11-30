from utils import read_input, run
import numpy as np

fname = "day11/input.txt"


def parse(fname):
    return np.array([
        [int(p) for p in row]
        for row in read_input(fname, types=[list])
    ])


##########
# PART 1 #
##########


def adjacent_coords(grid, i, j):
    min_i = max(i - 1, 0)
    max_i = min(i + 1, len(grid) - 1)
    min_j = max(j - 1, 0)
    max_j = min(j + 1, len(grid[i]) - 1)
    result = {(adj_i, adj_j) for adj_i in range(min_i, max_i + 1) for adj_j in range(min_j, max_j + 1)}
    result.remove((i, j))
    return list(result)



def increase(grid):
    return grid + 1


def flash(grid):
    flashed = np.zeros_like(grid)
    charged = (grid > 9).nonzero()

    while not np.all(flashed[charged]):
        for i, j in zip(*charged):
            for adj in adjacent_coords(grid, i, j):
                grid[adj] += 1
        flashed[charged] = 1
        charged = ((grid > 9) & (flashed == 0)).nonzero()

    grid[flashed == 1] = 0
    flashes = np.count_nonzero(flashed)
    return flashes
    


def part_one():
    grid = parse(fname)
    steps = 100
    flashes = 0
    for _ in range(steps):
        grid = increase(grid)
        flashes += flash(grid)

    return flashes


##########
# PART 2 #
##########


def part_two():
    grid = parse(fname)
    i = 0
    flashed = 0
    while flashed != grid.size:
        grid = increase(grid)
        flashed = flash(grid)
        i += 1

    return i


if __name__ == '__main__':
    run(part_one, part_two)