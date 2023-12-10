from utils import run
import numpy as np
from cachetools import cached
from cachetools.keys import hashkey
import sys

sys.setrecursionlimit(10000)


FNAME = "10/input.txt"


def parse_grid(input_file: str) -> np.ndarray:
    with open(input_file) as f:
        data = [
            list(line) for line in f.read().strip().split('\n')
        ]

        for i, line in enumerate(data):
            for j, char in enumerate(line):
                if char == 'S':
                    return (i, j), np.array(data)
    


##########
# PART 1 #
##########


PIPE_TO_BIN = {
    '|': '1010',
    '-': '0101',
    'L': '1100',
    'J': '1001',
    '7': '0011',
    'F': '0110',
    'S': '1111',
    '.': '0000',
}


def pipe_to_directions(pipe: str) -> list[bool]:
    return [bool(int(d)) for d in PIPE_TO_BIN[pipe]]


def adjacent_pipes(grid, coord):
    res = set()
    i, j = coord

    [north, east, south, west] = pipe_to_directions(grid[coord])

    if north and i > 0:
        res.add((i - 1, j))
    if south and i < len(grid) - 1:
        res.add((i + 1, j))
    if west and j > 0:
        res.add((i, j - 1))
    if east and j < len(grid[i]) - 1:
        res.add((i, j + 1))
    return res


def solve(initial, grid):
    distances = np.full(grid.shape, np.inf)
    distances[initial] = 0
    unvisited = {initial}
    visited = set()

    current = initial
    while unvisited:
        for neighbour in adjacent_pipes(grid, current):
            if grid[neighbour] != '.':
                distances[neighbour] = min(distances[current] + 1, distances[neighbour])
                if neighbour not in visited:
                    unvisited.add(neighbour)
        
        visited.add(current)
        unvisited.remove(current)
        if not unvisited:
            break
        current = min(unvisited, key=lambda u: distances[u])

    return distances


def part_one(input_file):
    start, grid = parse_grid(input_file)
    grid[start] = 'L'
    distances = solve(start, grid)
    return int(np.max(distances[distances != np.inf]))


##########
# PART 2 #
##########



@cached({}, key=lambda _g, _b, i, j: hashkey(i, j))
def search_basin(grid, basin, i, j):
    if grid[i][j] != np.inf:
        return basin
    
    basin.add((i, j))
    
    for adj_i, adj_j in adjacent_coords(grid, (i, j)):
        if (adj_i, adj_j) not in basin:
            search_basin(grid, basin, adj_i, adj_j)
    
    return basin


def adjacent_coords(grid, coord):
    res = []
    i, j = coord
    if i > 0:
        res.append((i - 1, j))
    if i < len(grid) - 1:
        res.append((i + 1, j))
    if j > 0:
        res.append((i, j - 1))
    if j < len(grid[i]) - 1:
        res.append((i, j + 1))
    return res


def is_touching_edge(basin, grid):
    return any(0 == c or c == axis - 1 for coord in basin for c, axis in zip(coord, grid.shape))


def part_two(input_file):
    start, grid = parse_grid(input_file)
    grid[start] = 'L'
    distances = solve(start, grid)

    grid[distances == np.inf] = 'O'

    basins = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            basins.add(frozenset(search_basin(distances, set(), i, j)))
    
    for basin in basins:
        if not is_touching_edge(basin, distances) and len(basin) > 10:
            for coord in basin:
                grid[coord] = 'I'

    with open('10/output.txt', 'w+') as f:
        for l in grid:
            f.writelines(''.join(map(str, l)) + '\n')


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
