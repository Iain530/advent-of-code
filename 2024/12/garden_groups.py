from utils import read_input, run
import numpy as np


FNAME = "12/input.txt"
Vector = tuple[int, int]
Grid = np.ndarray

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
PERPENDICULAR_DIRECTIONS = {
    UP: [LEFT, RIGHT],
    DOWN: [LEFT, RIGHT],
    LEFT: [UP, DOWN],
    RIGHT: [UP, DOWN]
}

def is_in_grid(coord: Vector, grid: Grid) -> bool:
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))


def add(v1: Vector, v2: Vector) -> Vector:
    return tuple(a + b for a, b in zip(v1, v2))


##########
# PART 1 #
##########


def get_neighbours(coord: Vector, directions=DIRECTIONS) -> list[Vector]:
    return [add(coord, direction) for direction in directions]


def is_same_group(v1: Vector, v2: Vector, grid: Grid) -> bool:
    return is_in_grid(v1, grid) and is_in_grid(v2, grid) and grid[v1] == grid[v2]


def find_group(point: Vector, grid: Grid, seen: set[Vector]) -> set[Vector]:
    if point in seen:
        return seen
    
    result = seen | {point}

    for n in get_neighbours(point):
        if is_same_group(point, n, grid):
            result |= find_group(n, grid, result)
    return result



def perimeter(group: set[Vector]) -> int:
    return sum(sum(1 for n in get_neighbours(point) if n not in group) for point in group)



def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    groups = []
    grouped = np.zeros(grid.shape, dtype=np.int32)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            point = (i, j)
            if not grouped[point]:
                group = find_group(point, grid, set())
                groups.append(group)
                for p in group:
                    grouped[p] = 1
    
    return sum(perimeter(group) * len(group) for group in groups)
            


    

    


##########
# PART 2 #
##########


def find_fence_group(point: Vector, fences: set[Vector], directions: list[Vector], seen: set[Vector]) -> set[Vector]:
    if point in seen:
        return seen
    
    result = seen | {point}
    neighbours = get_neighbours(point, directions)
    for n in neighbours:
        if n in fences:
            result |= find_fence_group(n, fences, directions, result)
    
    return result


def fences(group: set[Vector]) -> int:
    directional_fences = {
        direction: {point for point in group if add(point, direction) not in group}
        for direction in DIRECTIONS
    }
    
    result = 0
    for fence_direction in DIRECTIONS:
        counted = set()

        for point in directional_fences[fence_direction]:
            if point not in counted:
                counted |= find_fence_group(point, directional_fences[fence_direction], PERPENDICULAR_DIRECTIONS[fence_direction], set())
                result += 1
    
    return result
        

def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    groups = []
    grouped = np.zeros(grid.shape, dtype=np.int32)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            point = (i, j)
            if not grouped[point]:
                group = find_group(point, grid, set())
                groups.append(group)
                for p in group:
                    grouped[p] = 1
    
    return sum(fences(group) * len(group) for group in groups)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
