from utils import read_input, run
from functools import cache
import numpy as np


fname = "day15/input.txt"


def parse(fname):
    return [list(map(int, line)) for line in read_input(fname, types=[str])]


##########
# PART 1 #
##########


def adjacent_coords(grid, i, j):
    res = set()
    if i > 0:
        res.add((i - 1, j))
    if i < len(grid) - 1:
        res.add((i + 1, j))
    if j > 0:
        res.add((i, j - 1))
    if j < len(grid[i]) - 1:
        res.add((i, j + 1))
    return res


def dijkstra(grid):
    distances = np.full(grid.shape, np.inf)
    initial = (0, 0)
    distances[initial] = 0
    unvisited = {initial}
    visited = set()

    max_i = len(grid) - 1
    max_j = len(grid[0]) - 1
    end = (max_i, max_j)


    current = initial
    while current != end:

        for neighbour in adjacent_coords(grid, *current):
            if neighbour not in visited:
                dist = distances[current] + grid[neighbour]
                if dist < distances[neighbour]:
                    distances[neighbour] = dist
                unvisited.add(neighbour)
        
        visited.add(current)
        unvisited.remove(current)
        current = min(unvisited, key=lambda u: distances[u])

    return int(distances[end])


def part_one():
    grid = parse(fname)
    grid = np.array(grid, dtype=np.int64)
    return dijkstra(grid)


##########
# PART 2 #
##########


def build_cave(grid):
    res = grid
    for i in range(1, 5):
        new = (grid + i)
        new[new > 9] -= 9
        res = np.concatenate((res, new), axis=0)
    
    full_row = res
    
    for i in range(1, 5):
        new = (full_row + i)
        new[new > 9] -= 9
        res = np.concatenate((res, new), axis=1)
    
    return res


def part_two():
    grid = parse(fname)
    grid = np.array(grid, dtype=np.int64)
    grid = build_cave(grid)
    return dijkstra(grid)


if __name__ == '__main__':
    run(part_one, part_two)
