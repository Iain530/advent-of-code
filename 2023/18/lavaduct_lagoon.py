from utils import read_input, run
import numpy as np
from collections import deque

Vector = tuple[int, int]

FNAME = "18/input.txt"
UP = (-1, 0)
LEFT = (0, -1)
DOWN = (1, 0)
RIGHT = (0, 1)

DIRECTIONS = {
    'D': DOWN,
    'U': UP,
    'R': RIGHT,
    'L': LEFT,
}


def parse_line(line: str) -> tuple[Vector, int, str]:
    parts = line.split()
    return DIRECTIONS[parts[0]], int(parts[1]), parts[2].strip('()')



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


def search_basin(grid, i, j):
    queue = deque()
    basin = set()

    queue.append((i, j))
    while queue:
        i, j = queue.pop()
        if (i, j) in basin:
            continue

        if grid[i][j] == '#':
            continue
            
        basin.add((i, j))
        
        for adj_i, adj_j in adjacent_coords(grid, i, j):
            if (adj_i, adj_j) not in basin:
                queue.append((adj_i, adj_j))
        
    return basin


def add(v1: Vector, v2: Vector) -> Vector:
    return tuple(a + b for a, b in zip(v1, v2))


def shift_origin(trenches: dict[Vector, str]) -> dict[Vector, str]:
    min_x = min(x for x, _ in trenches.keys())
    min_y = min(y for _, y in trenches.keys())

    shift_by = (-min_x, -min_y)
    return {add(k, shift_by): v for k, v in trenches.items()}


def dig_trenches(data):
    trenches = dict()
    current = (0, 0)

    for direction, meters, color in data:
        for _ in range(meters):
            trenches[current] = color
            current = add(current, direction)
    
    return shift_origin(trenches)


def draw_trenches(trenches):
    max_x = max(x for x, _ in trenches.keys())
    max_y = max(y for _, y in trenches.keys())

    grid = np.full((max_x + 1, max_y + 1), '.')

    for coord, color in trenches.items():
        grid[coord] = '#'
    
    return grid


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    trenches = dig_trenches(data)

    grid = draw_trenches(trenches)
    basin = search_basin(grid, 83, 175)

    return len(trenches) + len(basin)
    



##########
# PART 2 #
##########


def part_two(input_file):
    pass


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
