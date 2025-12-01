from utils import read_input, run, Vector, add, DIRECTIONS, iter_grid
import numpy as np


FNAME = "20/input.txt"


##########
# PART 1 #
##########


def is_in_grid(coord, grid):
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))


def find_start(grid) -> Vector:
    for position in iter_grid(grid):
        if grid[position] == 'S':
            return position


def next_position(position, grid, path):
    return next((n for n in (add(position, d) for d in DIRECTIONS) if n not in path and walkable(n, grid)))


def find_path(start, grid):
    pos = start
    path = {}
    t = 0
    while grid[pos] != 'E':
        path[pos] = t
        t += 1
        pos = next_position(pos, grid, path)
    path[pos] = t
    return path


def walkable(position, grid):
    return is_in_grid(position, grid) and grid[position] != '#'


def cheats(position, grid, path, threshold=100) -> list[Vector]:
    return [n for n in (add(add(position, d), d) for d in DIRECTIONS) if walkable(n, grid) and n in path and path[n] >= path[position] + threshold + 2]


def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    start = find_start(grid)
    path = find_path(start, grid)
    return sum(1 for p in path for _ in cheats(p, grid, path, 100))
        


##########
# PART 2 #
##########


def manhattan_dist(p1, p2) -> int:
    return sum(abs(a - b) for a, b in zip(p1, p2))


def long_cheats(position, path, threshold = 100) -> set[Vector]:
    return {v for v in path if (dist := manhattan_dist(position, v)) <= 20 and path[v] >= path[position] + dist + threshold}


def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    start = find_start(grid)
    path = find_path(start, grid)
    return sum(1 for p in path for _ in long_cheats(p, path))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
