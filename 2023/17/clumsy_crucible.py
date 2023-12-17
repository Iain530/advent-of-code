from utils import read_input, run
from collections import deque
import numpy as np


FNAME = "17/input.txt"


def parse_line(line: str):
    return [int(c) for c in line]


##########
# PART 1 #
##########

Vector = tuple[int, int]
Step = tuple[Vector, Vector, int]
Grid = np.ndarray

UP = (-1, 0)
LEFT = (0, -1)
DOWN = (1, 0)
RIGHT = (0, 1)

OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

DIRECTIONS = [UP, LEFT, DOWN, RIGHT]


def opposite(direction: Vector) -> Vector:
    return OPPOSITE_DIRECTIONS[direction]


def is_in_grid(coord: Vector, grid: Grid) -> bool:
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))


def add(v1: Vector, v2: Vector) -> Vector:
    return tuple(a + b for a, b in zip(v1, v2))


def adjacent_steps(step: Step) -> list[tuple[Step, int]]:
    coord, direction, straight = step
    result = []
    for next_direction in DIRECTIONS:
        if next_direction == direction:
            if straight < 3:
                result.append((add(coord, next_direction), next_direction, straight + 1))
        elif next_direction != opposite(direction):
            result.append((add(coord, next_direction), next_direction, 1))

    return result




def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=parse_line))
    end = add(grid.shape, (-1, -1))
    best = np.inf
    queue = deque()
    seen = dict()
    start = ((0, 0), RIGHT, 0)

    queue.append((start, 0))
    while queue:
        step, loss = queue.pop()
        if loss > best:
            continue

        if step[0] == end:
            continue

        if step in seen and seen[step] <= loss:
            continue
        seen[step] = loss

        for next_step in adjacent_steps(step):
            if is_in_grid(next_step[0], grid):
                queue.append((next_step, loss + grid[next_step[0]]))
    
    return best


##########
# PART 2 #
##########


def adjacent_ultra_steps(step: Step) -> list[tuple[Step, int]]:
    coord, direction, straight = step
    result = []
    for next_direction in DIRECTIONS:
        if next_direction == direction:
            if straight < 10:
                result.append((add(coord, next_direction), next_direction, straight + 1))
        elif next_direction != opposite(direction):
            if straight >= 4:
                result.append((add(coord, next_direction), next_direction, 1))

    return result


def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=parse_line))
    end = add(grid.shape, (-1, -1))
    best = np.inf
    queue = deque()
    seen = dict()
    start = ((0, 0), RIGHT, 0)

    queue.append((start, 0))
    while queue:
        step, loss = queue.pop()
        if loss > best:
            print(best, len(queue))
            continue

        if step[0] == end and step[2] >= 4:
            best = min(best, loss)
            continue

        if step in seen and seen[step] <= loss:
            continue
        seen[step] = loss

        for next_step in adjacent_ultra_steps(step):
            if is_in_grid(next_step[0], grid):
                queue.append((next_step, loss + grid[next_step[0]]))
    return best


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
