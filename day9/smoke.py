from utils import read_input, run
from functools import reduce
from operator import mul
from cachetools import cached
from cachetools.keys import hashkey


fname = "day9/input.txt"


def parse(fname):
    return [
        [int(p) for p in row]
        for row in read_input(fname, types=[list])
    ]


##########
# PART 1 #
##########


def adjacent_coords(grid, i, j):
    res = []
    if i > 0:
        res.append((i - 1, j))
    if i < len(grid) - 1:
        res.append((i + 1, j))
    if j > 0:
        res.append((i, j - 1))
    if j < len(grid[i]) - 1:
        res.append((i, j + 1))
    return res


def is_low_point(grid, i, j):
    value = grid[i][j]
    return all(grid[adj_i][adj_j] > value for adj_i, adj_j in adjacent_coords(grid, i, j))


def part_one():
    grid = parse(fname)

    low_points = [value for i in range(len(grid)) for j, value in enumerate(grid[i]) if is_low_point(grid, i, j)]

    return sum(low_points) + len(low_points)


##########
# PART 2 #
##########


@cached({}, key=lambda _g, _b, i, j: hashkey(i, j))
def search_basin(grid, basin, i, j):
    if grid[i][j] == 9:
        return basin
    
    basin.add((i, j))
    
    for adj_i, adj_j in adjacent_coords(grid, i, j):
        if (adj_i, adj_j) not in basin:
            search_basin(grid, basin, adj_i, adj_j)
    
    return basin


def part_two():
    grid = parse(fname)
    basins = set()

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            basins.add(frozenset(search_basin(grid, set(), i, j)))

    return reduce(mul, sorted(map(len, basins))[-3:], 1)


if __name__ == '__main__':
    run(part_one, part_two)
