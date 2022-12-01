from timeit import default_timer as timer
from typing import Callable, TypeVar, Any


T = TypeVar('T')


def default_parse_line(line: str) -> list[str]:
    return line.strip().split()


def read_input(fname: str, separator: str = '\n', parse_chunk: Callable[[str], T] = default_parse_line) -> list[T]:
    with open(fname) as f:
        return [parse_chunk(line) for line in f.read().split(separator)]


def timed(f, *args, **kwargs):
    t1 = timer()
    result = f(*args, **kwargs)
    t2 = timer()
    return result, t2 - t1


def run(part_one, part_two):
    print("PART 1")
    result, time = timed(part_one)
    print(f"Answer:\t{result}\nTime:\t{time*1000}ms")
    print()
    print(f"PART 2")
    result, time = timed(part_two)
    print(f"Answer:\t{result}\nTime:\t{time*1000}ms")
