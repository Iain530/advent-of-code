from utils import read_input, run, UP, DOWN, LEFT, RIGHT, DIRECTIONS, Vector, iter_grid, add
import numpy as np


FNAME = "15/input.txt"
Grid = np.ndarray


ARROW_TO_DIRECTON = {
    '^': UP,
    '>': RIGHT,
    '<': LEFT,
    'v': DOWN,
}


def parse_input(input_file) -> tuple[Grid, list[Vector], Vector]:
    raw_grid, raw_directions = read_input(input_file, separator='\n\n')
    grid = np.array([list(l) for l in raw_grid])
    directions = [ARROW_TO_DIRECTON[char] for char in ''.join(raw_directions)]

    return grid, directions



##########
# PART 1 #
##########

def find_start(grid: Grid) -> Vector:
    for point in iter_grid(grid):
        if grid[point] == '@':
            return point


def can_move(grid, position, direction) -> bool:
    new_position = add(position, direction)
    if grid[new_position] == '.':
        return True
    
    if grid[new_position] == 'O':
        return can_move(grid, new_position, direction)
    
    return False


def move(grid: Grid, position: Vector, direction: Vector) -> Vector:
    new_position = add(position, direction)

    if grid[new_position] == '#':
        return position

    if grid[new_position] != '.':
        move(grid, new_position, direction)

    if grid[new_position] == '.':
        grid[new_position] = grid[position]
        grid[position] = '.'
        return new_position


def gps_coordinate(box: Vector):
    return 100 * box[0] + box[1]


def show(grid: Grid):
    for line in grid:
        print(''.join(line))
    


def part_one(input_file):
    grid, directions = parse_input(input_file)
    position = find_start(grid)

    for direction in directions:
        if can_move(grid, position, direction):
            position = move(grid, position, direction)
    
    return sum(gps_coordinate(point) for point in iter_grid(grid) if grid[point] == 'O')



##########
# PART 2 #
##########


def scale_grid(grid):
    x, y = grid.shape
    new_grid = np.zeros((x, y * 2), dtype=str)

    def replace(point, match, new):
        if grid[point] == match:
            new_x = point[0]
            new_y = point[1] * 2
            new_grid[new_x,new_y] = new[0]
            new_grid[new_x,new_y+1] = new[1]

    for point in iter_grid(grid):
        replace(point, '#', '##')
        replace(point, 'O', '[]')
        replace(point, '.', '..')
        replace(point, '@', '@.')
    
    return new_grid


def can_move_wide(grid, position, direction) -> bool:
    new_position = add(position, direction)
    if grid[new_position] == '.':
        return True
    
    if grid[new_position] in ('[', ']'):
        if direction in (UP, DOWN):
            other_half = add(new_position, RIGHT if grid[new_position] == '[' else LEFT)
            return can_move_wide(grid, new_position, direction) and can_move_wide(grid, other_half, direction)
        return can_move_wide(grid, new_position, direction)

    return False


def move_wide(grid: Grid, position: Vector, direction: Vector, moved: set) -> Vector:
    new_position = add(position, direction)

    if position in moved:
        return

    if grid[new_position] == '#':
        return position

    if grid[new_position] in ('[', ']'):
        if direction in (UP, DOWN):
            other_half = add(new_position, RIGHT if grid[new_position] == '[' else LEFT)
            move_wide(grid, other_half, direction, moved)
        move_wide(grid, new_position, direction, moved)

    if grid[new_position] == '.':
        grid[new_position] = grid[position]
        grid[position] = '.'
        moved.add(position)
        return new_position


def part_two(input_file):
    grid, directions = parse_input(input_file)
    grid = scale_grid(grid)
    position = find_start(grid)

    for direction in directions:
        if can_move_wide(grid, position, direction):
            position = move_wide(grid, position, direction, set())

    return sum(gps_coordinate(point) for point in iter_grid(grid) if grid[point] == '[')


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
