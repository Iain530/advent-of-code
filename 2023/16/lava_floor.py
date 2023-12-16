from utils import read_input, run
from itertools import chain
import numpy as np


FNAME = "16/input.txt"
Vector = tuple[int, int]
Beam = tuple[Vector, Vector]
Grid = np.ndarray


##########
# PART 1 #
##########


UP = (-1, 0)
LEFT = (0, -1)
DOWN = (1, 0)
RIGHT = (0, 1)


DIRECTIONS = [UP, LEFT, DOWN, RIGHT]
HORIZONTAL_DIRECTIONS = {LEFT, RIGHT}
VERTICAL_DIRECTIONS = {UP, DOWN}


def lrot(direction: Vector) -> Vector:
    return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]


def rrot(direction: Vector) -> Vector:
    return DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 4]


def is_in_grid(coord: Vector, grid: Grid) -> bool:
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))


def add(v1: Vector, v2: Vector) -> Vector:
    return tuple(a + b for a, b in zip(v1, v2))


def filter_in_grid(beams: list[Beam], grid: Grid) -> list[Beam]:
    return [beam for beam in beams if is_in_grid(beam[0], grid)]


def move(beam: Beam) -> Beam:
    coord, direction = beam
    return (add(coord, direction), direction)


def turn_and_split(beam: Beam, grid: Grid) -> list[Beam]:
    current, direction = beam
    space = grid[current]

    if space == '/':
        rot = lrot if direction in HORIZONTAL_DIRECTIONS else rrot
        return [(current, rot(direction))]
    
    if space == '\\':
        rot = rrot if direction in HORIZONTAL_DIRECTIONS else lrot
        return [(current, rot(direction))]
    
    if space == '|' and direction in HORIZONTAL_DIRECTIONS:
        return [(current, d) for d in VERTICAL_DIRECTIONS]
    
    if space == '-' and direction in VERTICAL_DIRECTIONS:
        return [(current, d) for d in HORIZONTAL_DIRECTIONS]
    
    return [beam]


def step(beams: list[Beam], grid: Grid) -> list[Beam]:
    return filter_in_grid(
        [move(beam) for beam in chain.from_iterable(
            turn_and_split(beam, grid) for beam in beams
        )],
        grid
    )


def solve(start: Beam, grid: Grid) -> int:
    energised = np.zeros(grid.shape)
    beams = [start]

    seen = set()

    while beams:
        for beam in beams:
            energised[beam[0]] = 1
            seen.add(beam)
        beams = [beam for beam in step(beams, grid) if beam not in seen]
    
    return len(list(filter(bool, (energised == 1).flatten())))


def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    start = ((0, 0), RIGHT)
    return solve(start, grid)


##########
# PART 2 #
##########


def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    best = 0

    def check(start):
        nonlocal best
        if (ans := solve(start, grid)) > best:
            best = ans

    for i in range(grid.shape[0]):
        check(((i, 0), RIGHT))
        check(((i, grid.shape[1] - 1), LEFT))
    
    for i in range(grid.shape[1]):
        check(((i, 0), DOWN))
        check(((i, grid.shape[0] - 1), UP))

    return best


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
