from timeit import default_timer as timer
from typing import Callable, TypeVar, Any


T = TypeVar('T')


def default_parse_line(line: str) -> list[str]:
    return line.strip().split()


def read_input(fname: str, separator: str = '\n', parse_chunk: Callable[[str], T] = default_parse_line) -> list[T]:
    with open(fname) as f:
        return [parse_chunk(line) for line in f.read().strip().split(separator)]


def timed(f, *args, **kwargs):
    t1 = timer()
    result = f(*args, **kwargs)
    t2 = timer()
    return result, t2 - t1


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
        print(f"Passed - {test_name} in {time*1000}ms")
    else:
        print(f"Failed - {test_name or test_input_file}\nExpected {expected}, got {result} in {time*1000}ms")
        if exit_on_fail:
            exit(1)
