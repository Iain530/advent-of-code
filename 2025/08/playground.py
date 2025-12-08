from utils import read_input, run
from itertools import permutations
from functools import reduce
from operator import mul
import math


FNAME = "08/input.txt"

Point = tuple[int, int, int]


def parse_line(line: str) -> Point:
    return tuple(map(int, line.split(',')))


next_circuit_id = 1


##########
# PART 1 #
##########


def calc_distance(p1: Point, p2: Point) -> float:
    return math.sqrt(sum((a2 - a1) ** 2 for a1, a2 in zip(p1, p2)))


def create_circuit():
    global next_circuit_id
    result = next_circuit_id
    next_circuit_id += 1
    return result


def connect(p1: Point, p2: Point, circuits_by_point: dict[Point, int], circuits_by_id: dict[int, set]):
    c1 = circuits_by_point[p1]
    c2 = circuits_by_point[p2]
    if c1 == c2:
        return

    for p in circuits_by_id[c2]:
        circuits_by_id[c1].add(p)
        circuits_by_point[p] = c1
    
    del circuits_by_id[c2]


def part_one(input_file):
    points = read_input(input_file, parse_chunk=parse_line)

    circuits_by_point = {p: i for i, p in enumerate(points)}
    circuits_by_id = {v: set((k,)) for k, v in circuits_by_point.items()}
    distances = {
        frozenset({p1, p2}): calc_distance(p1, p2) for p1, p2 in permutations(points, 2)
    }
    sorted_points = sorted(distances.keys(), key=lambda k: distances[k])

    for i in range(1000):
        p1, p2 = sorted_points[i]
        connect(p1, p2, circuits_by_point, circuits_by_id)
    

    circuit_sizes = sorted(map(len, circuits_by_id.values()))
    return reduce(mul, circuit_sizes[-3:])



##########
# PART 2 #
##########


def part_two(input_file):
    points = read_input(input_file, parse_chunk=parse_line)
    circuits_by_point = {p: i for i, p in enumerate(points)}
    circuits_by_id = {v: set((k,)) for k, v in circuits_by_point.items()}
    distances = {
        frozenset({p1, p2}): calc_distance(p1, p2) for p1, p2 in permutations(points, 2)
    }
    sorted_points = sorted(distances.keys(), key=lambda k: distances[k])

    i = 0
    while len(circuits_by_id) > 1:
        p1, p2 = sorted_points[i]
        connect(p1, p2, circuits_by_point, circuits_by_id)
        i += 1
    
    return p1[0] * p2[0]


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
