import re
import numpy as np
from utils import read_input, run, run_test


FNAME = "22/input.txt"

VOID = 0
WALKABLE = 1
WALL = 2

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)

DIRECTIONS = [RIGHT, DOWN, LEFT, UP]


def parse_input(input_file):
    raw_map, raw_steps = read_input(input_file, separator='\n\n', parse_chunk=lambda l: l.splitlines())
    grid = np.zeros((len(raw_map), max(len(row) for row in raw_map)))
    for i, row in enumerate(raw_map):
        for j, char in enumerate(row):
            if char == '.':
                grid[i, j] = WALKABLE
            elif char == '#':
                grid[i, j] = WALL
    
    steps = [(int(dist), 1 if rot == 'R' else -1) for dist, rot in re.findall(r"([0-9]+)([LR]+)", raw_steps[0], re.I)]
    steps.append((14, 0))
    return grid, steps


##########
# PART 1 #
##########


def find_start(grid):
    for i, tile in enumerate(grid[0]):
        if tile == WALKABLE:
            return (0, i)


def add(grid, pos, direction):
    return tuple((a + b) % grid.shape[i] for i, (a, b) in enumerate(zip(pos, direction)))


def next_tile(grid, pos, direction):
    tile = add(grid, pos, direction)
    while grid[tile] == VOID:
        tile = add(grid, tile, direction)
    return tile


def move(grid, pos, dist, direction):
    new_pos = pos
    for _ in range(dist):
        tile = next_tile(grid, new_pos, direction)
        if grid[tile] == WALL:
            break
        new_pos = tile
    return new_pos


def rotate(direction, rot):
    return DIRECTIONS[(DIRECTIONS.index(direction) + rot) % 4]


def part_one(input_file):
    grid, steps = parse_input(input_file)
    
    pos = find_start(grid)
    direction = RIGHT

    for dist, rot in steps:
        pos = move(grid, pos, dist, direction)
        direction = rotate(direction, rot)
        print(f"Moved {dist}, rotated {rot}, {direction=} {pos=}")

    row, col = pos

    return (row + 1) * 1000 + (col + 1) * 4 + DIRECTIONS.index(direction)


##########
# PART 2 #
##########


def cube_face(pos):
    return tuple(a // 50 for a in pos)


def wrap_direction(current_face, next_face):
    
    if current_face == (0, 2):
        if next_face == (0, 0):
            return LEFT
        if next_face == (1, 2):
            return LEFT
        if next_face == (2, 2):
            return UP
    
    if current_face == (0, 1):
        if next_face == (0, 0):
            return 
        if next_face == (2, 1):
            return
    
    if current_face == (1, 1):
        if next_face == (1, 0):
            return
        if next_face == (1, 2):
            return
    
    # if current_face 


def wrap_position(current_face, next_face, pos):
    pass


def next_cube_tile(grid, pos, direction):
    tile = add(grid, pos, direction)
    if grid[tile] == VOID:
        current_face = cube_face(pos)
        next_face = cube_face(tile)
        
        direction = 
        
    return tile, direction


def move_on_cube(grid, pos, dist, direction):
    new_pos = pos
    for _ in range(dist):
        tile, new_direction = next_cube_tile(grid, new_pos, direction)
        if grid[tile] == WALL:
            break
        new_pos = tile
        direction = new_direction
    return new_pos, direction


def part_two(input_file):
    grid, steps = parse_input(input_file)
    
    pos = find_start(grid)
    direction = RIGHT

    for dist, rot in steps:
        pos, direction = move_on_cube(grid, pos, dist, direction)
        direction = rotate(direction, rot)
        print(f"Moved {dist}, rotated {rot}, {direction=} {pos=}")

    row, col = pos

    return (row + 1) * 1000 + (col + 1) * 4 + DIRECTIONS.index(direction)


if __name__ == '__main__':
    run_test(part_one, '22/test_input.txt', 6032, 'Example input')
    run(part_one, part_two, FNAME)
