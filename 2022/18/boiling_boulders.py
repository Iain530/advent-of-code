import numpy as np
from utils import read_input, run
from collections import deque


FNAME = "18/input.txt"


def create_grid(data):
    grid = np.zeros((22, 22, 22))
    for coord in data:
        grid[coord] = 1
    return grid


##########
# PART 1 #
##########


def find_neighbours(grid, coord):
    x, y, z = coord
    return [
        (x+1, y, z),
        (x-1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1),
    ]


def count_surface_area(grid, coord):
    return sum(not grid[n] for n in find_neighbours(grid, coord))


def part_one(input_file):
    data = read_input(input_file, parse_chunk=lambda l: tuple(int(n) for n in l.split(',')))
    grid = create_grid(data)
    return sum(count_surface_area(grid, c) for c in data)


##########
# PART 2 #
##########


def count_exposed_surface_area(grid, coord, exposed):
    return sum(int(exposed[n]) for n in find_neighbours(grid, coord))


def find_exposed(grid):
    exposed = np.zeros(grid.shape)
    queue = deque()
    queue.append((0, 0, 0))

    while queue:
        coord = queue.pop()
        if not grid[coord]:
            exposed[coord] = 1
            for n in find_neighbours(grid, coord):
                if all(0 <= n[i] < grid.shape[i] for i in range(3)) and not exposed[n]:
                    queue.append(n)
    
    return exposed


def part_two(input_file):
    data = read_input(input_file, parse_chunk=lambda l: tuple(int(n) for n in l.split(',')))
    grid = create_grid(data)
    exposed = find_exposed(grid)
    return sum(count_exposed_surface_area(grid, c, exposed) for c in data)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
