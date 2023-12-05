from utils import read_input, run
from functools import reduce
from itertools import chain
from typing import TypeVar, Iterable

FNAME = "05/input.txt"

##########
# PART 1 #
##########


def parse_chunk(paragraph: str):
    if paragraph.startswith('seeds: '):
        return [int(s) for s in paragraph.split(': ')[1].split()]

    maps = [
        [int(n) for n in line.split()]
        for line in paragraph.split('\n')[1:]
    ]

    def apply_map(input):
        for dest, source, rng in maps:
            if source <= input < source + rng:
                return input + (dest - source)
        return input

    return apply_map


def part_one(input_file):
    seeds, *maps = read_input(input_file, parse_chunk=parse_chunk, separator='\n\n')

    def apply(input, map_fn):
        return map_fn(input)

    return min(reduce(apply, maps, seed) for seed in seeds)

##########
# PART 2 #
##########

Line = tuple[int, int]
Transform = tuple[int, Line]
T = TypeVar('T')

def parse_part_2(paragraph: str):
    if paragraph.startswith('seeds: '):
        seeds = []
        rest = list(map(int, paragraph.split(': ')[1].split()))
        while len(rest):
            start, length, *rest = rest
            seeds.append((start, length))
        return seeds

    maps = [
        [int(n) for n in line.split()]
        for line in paragraph.split('\n')[1:]
    ]

    return sorted([
        ((move - start), (start, length))
        for move, start, length in maps
    ], key=lambda t: t[1][0])


def flatten(iterable: Iterable[Iterable[T]]) -> list[T]:
    return list(chain.from_iterable(iterable))


def split(line: Line, pivot: int) -> list[Line]:
    start, length = line
    if start <= pivot < start + length:
        new_length = pivot - start
        return [(start, new_length), (pivot, length - new_length)]
    return [line]


def sort(lines: list[Line]) -> list[Line]:
    return sorted(lines, key=lambda l: l[0])


def is_overlapping(l1: Line, l2: Line) -> bool:
    l1_start, l1_length = l1
    l2_start, l2_length = l2
    return l1_start <= l2_start < l1_start + l1_length or l2_start <= l1_start < l2_start + l2_length


def pivot_in_line(line: Line, pivot: int) -> bool:
    return line[0] < pivot < line[0] + line[1]


def merge(l1: Line, l2: Line) -> Line:
    l1_start, l1_length = l1
    l2_start, l2_length = l2
    start = min(l1_start, l2_start)
    length = max(l1_start + l1_length, l2_start + l2_length) - start
    return start, length


def get_pivots(transforms: list[Transform]) -> list[int]:
    return sorted(set(flatten(
        [start, start + length]
        for _, (start, length) in transforms
    )))


def split_on_pivots(line: Line, pivots: list[int]) -> list[Line]:
    for pivot in pivots:
        if pivot_in_line(line, pivot):
            l1, l2 = split(line, pivot)
            return [l1] + split_on_pivots(l2, pivots)
    return [line]


def split_all_lines(lines: list[Line], transforms: list[Transform]) -> list[Line]:
    pivots = get_pivots(transforms)
    return sort(flatten(
        split_on_pivots(line, pivots) for line in lines
    ))


def apply_transforms(line: Line, transforms: list[Transform]) -> Line:
    for diff, transform_line in transforms:
        if is_overlapping(line, transform_line):
            return (line[0] + diff, line[1])
    return line


def process_map(lines: list[Line], transforms: list[Transform]) -> list[Line]:
    split_lines = split_all_lines(lines, transforms)
    return [apply_transforms(line, transforms) for line in split_lines]


def part_two(input_file):
    lines, *maps = read_input(input_file, parse_chunk=parse_part_2, separator='\n\n')
    for m in maps:
        lines = process_map(lines, m)
    return min(start for start, _ in lines)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
