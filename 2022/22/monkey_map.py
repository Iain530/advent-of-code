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

CUBE_SIZE = 50
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


def add_and_wrap(grid, pos, direction):
    return tuple((a + b) % grid.shape[i] for i, (a, b) in enumerate(zip(pos, direction)))


def next_tile(grid, pos, direction):
    tile = add_and_wrap(grid, pos, direction)
    while grid[tile] == VOID:
        tile = add_and_wrap(grid, tile, direction)
    return tile


def move(grid, pos, dist, direction):
    new_pos = pos
    for _ in range(dist):
        tile = next_tile(grid, new_pos, direction)
        if grid[tile] == WALL:
            break
        new_pos = tile
    return new_pos


def rotate_direction(direction, rot):
    return DIRECTIONS[(DIRECTIONS.index(direction) + rot) % 4]


def part_one(input_file):
    grid, steps = parse_input(input_file)
    
    pos = find_start(grid)
    direction = RIGHT

    for dist, rot in steps:
        pos = move(grid, pos, dist, direction)
        direction = rotate_direction(direction, rot)
        print(f"Moved {dist}, rotated {rot}, {direction=} {pos=}")

    row, col = pos

    return (row + 1) * 1000 + (col + 1) * 4 + DIRECTIONS.index(direction)


##########
# PART 2 #
##########


def add(pos, direction):
    return tuple(a + b for a, b in zip(pos, direction))


def cube_face(pos):
    return tuple(a // CUBE_SIZE for a in pos)


def cube_face_to_real(face):
    return tuple(a * CUBE_SIZE for a in face)


def cube_position(pos):
    return tuple(a % CUBE_SIZE for a in pos)


def in_grid(grid, coord):
    return all(0 <= coord[i] < grid.shape[i] for i in range(2))


def rotate_cube_position(pos, rots):
    for _ in range(rots):
        x, y = pos
        pos = (y, CUBE_SIZE - 1 - x)
    return pos


# TODO: need current face as well
WRAP_FACE = {
    (-1, 1): ((3, 0), 1),
    (-1, 2): ((3, 0), 0),
    (0, 0): ((2, 0), 2),
    (0, 3): ((2, 1), 2),
    (1, 0): ((2, 0), 3),
    (1, 2): ((0, 2), 3),
    (2, -1): ((0, 1), 2),
    (2, 2): ((0, 2), 2),
    (3, -1): ((0, 1), 3),
    (3, 1): ((2, 1), 3),
    (4, 0): ((0, 2), 0),
}


def wrap_face(current_face, next_face):
    match (current_face, next_face):
        case _, (-1, 1): return ((3, 0), 1)
        case _, (-1, 2): return ((3, 0), 0)
        case _, (0, 0): return ((2, 0), 2)
        case _, (0, 3): return ((2, 1), 2)
        case (1, 1), (1, 0): return ((2, 0), 3)
        case (2, 0), (1, 0): return ((1, 1), 1)
        case (1, 1), (1, 2): return ((0, 2), 3)
        case (0, 2), (1, 2): return ((1, 1), 1)
        case _, (2, -1): return ((0, 1), 2)
        case _, (2, 2): return ((0, 2), 2)
        case _, (3, -1): return ((0, 1), 3)
        case (3, 0), (3, 1): return ((2, 1), 3)
        case (2, 1), (3, 1): return ((3, 0), 1)
        case _, (4, 0): return ((0, 2), 0)
        case _: raise Exception()


def wrap_position(prev_face, pos, direction):
    relative_pos = cube_position(pos)
    face = cube_face(pos)
    next_face, rots = wrap_face(prev_face, face)
    new_pos = add(cube_face_to_real(next_face), rotate_cube_position(relative_pos, rots))
    new_dir = rotate_direction(direction, rots)
    # print(f'Wrapping {pos=} {face=} {direction=} to {new_pos=} {new_dir=}')
    return new_pos, new_dir


def next_cube_tile(grid, pos, direction):
    tile = add(pos, direction)
    if not in_grid(grid, tile) or grid[tile] == VOID:
        tile, direction = wrap_position(cube_face(pos), tile, direction)
        
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
        direction = rotate_direction(direction, rot)
        # print(f"Moved {dist}, rotated {rot}, {direction=} {pos=}")

    row, col = pos
    return (row + 1) * 1000 + (col + 1) * 4 + DIRECTIONS.index(direction)


if __name__ == '__main__':
    run_test(part_one, '22/test_input.txt', 6032, 'Example input')
    run(part_one, part_two, FNAME)
