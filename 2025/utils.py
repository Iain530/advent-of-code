from timeit import default_timer as timer
from itertools import tee
from typing import Callable, TypeVar, Any


T = TypeVar('T')
Vector = tuple[int, int]

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


def default_parse_line(line: str) -> list[str]:
    return line.strip().split()


def read_input(fname: str, separator: str = '\n', parse_chunk: Callable[[str], T] = default_parse_line) -> list[T]:
    with open(fname) as f:
        return [parse_chunk(line) for line in f.read().rstrip().split(separator)]


def timed(f, *args, **kwargs):
    t1 = timer()
    result = f(*args, **kwargs)
    t2 = timer()
    return result, t2 - t1


def sliding_window(iterable, size):
    iterables = tee(iterable, size)
    for i, iterator in enumerate(iterables):
        for _ in range(i):
            next(iterator)
    return zip(*iterables)


def run(part_one, part_two, input_file):
    print("PART 1")
    result, time = timed(part_one, input_file)
    print(f"Answer:\t{result}\nTime:\t{time*1000}ms")
    print()
    print(f"PART 2")
    result, time = timed(part_two, input_file)
    print(f"Answer:\t{result}\nTime:\t{time*1000}ms")


def run_test(part, test_input_file, expected, test_name: str = "", exit_on_fail: bool = True):
    result, time = timed(part, test_input_file)
    if result == expected:
        print(f"Passed: {test_name} in {time*1000}ms")
    else:
        print(f"Failed: {test_name or test_input_file}\nExpected {expected}, got {result} in {time*1000}ms")
        if exit_on_fail:
            exit(1)


def iter_grid(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            yield (i, j)


def is_in_grid(coord, grid):
    return all(0 <= c < axis for c, axis in zip(coord, grid.shape))



def add(v1: Vector, v2: Vector) -> Vector:
    return tuple(a + b for a, b in zip(v1, v2))