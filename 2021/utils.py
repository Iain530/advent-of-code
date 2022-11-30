from typing import List, Type, Generator
from timeit import default_timer as timer


def read_input(fname: str, types: List[Type] = None) -> Generator:
    with open(fname) as f:
        lines = (line.strip().split() for line in f.readlines())

    if types is None:
        yield from lines
    else:
        if len(types) > 1:
            for line in lines:
                yield tuple(typ(val) for typ, val in zip(types, line))
        else:
            for line in lines:
                yield types[0](line[0])


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
