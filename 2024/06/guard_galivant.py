from utils import read_input, run
import numpy as np


FNAME = "06/input.txt"

Vector = tuple[int, int]
Grid = np.ndarray

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


def parse_input(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[(i, j)] == '^':
                grid[(i, j)] = '.'
                return (i, j), grid

##########
# PART 1 #
##########


def is_in_grid(coord: Vector, grid: Grid) -> bool:
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))


def add(v1: Vector, v2: Vector) -> Vector:
    return tuple(a + b for a, b in zip(v1, v2))


def next_position(position, grid, direction_i, obstruction=None) -> tuple[Vector, int]:
    next_pos = add(position, DIRECTIONS[direction_i])
    if not is_in_grid(next_pos, grid):
        return
    
    next_direction = direction_i
    while grid[next_pos] == '#' or next_pos == obstruction:
        next_direction = (next_direction + 1) % 4
        next_pos = add(position, DIRECTIONS[next_direction])
        if not is_in_grid(next_pos, grid):
            return
    
    return next_pos, next_direction



def part_one(input_file):
    position, grid = parse_input(input_file)
    direction_index = 0
    seen = set()
    print(grid.shape)

    while result := next_position(position, grid, direction_index):
        position, direction_index = result
        seen.add(position)
    
    return len(seen)



##########
# PART 2 #
##########


def rotate_and_step(position, direction, grid):
    next_direction = (direction + 1) % 4
    next_pos = add(position, DIRECTIONS[next_direction])
    while grid[next_pos] == '#':
        next_direction = (direction + 1) % 4
        next_pos = add(position, DIRECTIONS[next_direction])
    return next_pos, next_direction


def can_create_cycle_at(position, direction, grid, visited, path) -> bool:
    next_pos, next_dir = rotate_and_step(position, direction, grid)
    block = add(position, DIRECTIONS[direction])
    return (next_pos, next_dir) in path and is_in_grid(block, grid) and block not in visited


def can_escape(position, grid, direction, obstruction):
    path = set()
    path.add((position, direction))

    while result := next_position(position, grid, direction, obstruction):
        position, direction = result
        if (position, direction) in path:
            return False
        path.add((position, direction))

    return True


def part_two(input_file):
    position, grid = parse_input(input_file)
    direction_index = 0
    visited = set()
    visited.add(position)
    obstructions = set()


    while result := next_position(position, grid, direction_index):
        if result[0] not in visited and result[0] not in obstructions and not can_escape(position, grid, direction_index, result[0]):
            obstructions.add(result[0])

        position, direction_index = result
        visited.add(position)
        
    return len(obstructions)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
