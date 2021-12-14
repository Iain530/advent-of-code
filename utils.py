from typing import List, Type, Generator


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
