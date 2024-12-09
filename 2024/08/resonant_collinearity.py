from utils import read_input, run
import numpy as np
from collections import defaultdict
from itertools import combinations


FNAME = "08/input.txt"
Vector = tuple[int, int]
Grid = np.ndarray


def parse_input(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    antennas = defaultdict(list)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[(i, j)] != '.':
                antennas[grid[(i, j)]].append((i, j))
    
    return antennas, grid

##########
# PART 1 #
##########


def is_in_grid(coord: Vector, grid: Grid) -> bool:
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))


def add(v1: Vector, v2: Vector) -> Vector:
    return tuple(a + b for a, b in zip(v1, v2))


def diff(v1: Vector, v2: Vector) -> Vector:
    return tuple(a - b for a, b in zip(v1, v2))


def mul(v: Vector, s: int) -> Vector:
    return tuple(a * s for a in v)


def find_antinodes(antenna_pair: tuple[Vector, Vector]) -> set[Vector]:
    a, b = antenna_pair
    return {add(b, diff(b, a)), add(a, diff(a, b))}


def part_one(input_file):
    antennas, grid = parse_input(input_file)
    antinodes = set()
    for frequency in antennas.values():
        for antenna_pair in combinations(frequency, 2):
            antinodes |= find_antinodes(antenna_pair)
    
    return len(set(filter(lambda n: is_in_grid(n, grid), antinodes)))



##########
# PART 2 #
##########


def extrapolate(a, b, grid) -> set[Vector]:
    dist = diff(b, a)
    node = add(b, dist)
    result = {a, b}
    while is_in_grid(node, grid):
        result.add(node)
        node = add(node, dist)
    
    return result


def find_antinodes_part_2(antenna_pair: tuple[Vector, Vector], grid) -> set[Vector]:
    a, b = antenna_pair
    result = set()
    result |= extrapolate(a, b, grid)
    result |= extrapolate(b, a, grid)
    return result


def part_two(input_file):
    antennas, grid = parse_input(input_file)
    antinodes = set()
    for frequency in antennas.values():
        for antenna_pair in combinations(frequency, 2):
            antinodes |= find_antinodes_part_2(antenna_pair, grid)
    
    return len(antinodes)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
