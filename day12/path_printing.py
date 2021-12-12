from utils import read_input
from dataclasses import dataclass
from typing import List, Optional, Set, Dict, Tuple
from itertools import permutations
from cachetools import cached
from cachetools.keys import hashkey

fname = "day12/input.txt"


@dataclass(init=False)
class Cave:
    name: str
    big: bool
    outgoing: Set[str]

    def __init__(self, name: str) -> None:
        self.name = name
        self.big = name.isupper()
        self.outgoing = set()


@dataclass(init=False)
class Maze:
    caves: Dict[str, Cave]

    def __init__(self, paths: List[str]) -> None:
        caves = dict()
        for path in paths:
            for base, out in permutations(path.split('-')):
                if base not in caves:
                    caves[base] = Cave(base)
                caves[base].outgoing.add(out)
        self.caves = caves
    

    def outgoing_caves(self, name: str) -> List[Cave]:
        return [self[out] for out in self[name].outgoing]


    def __getitem__(self, name: str) -> Cave:
        return self.caves[name]


def parse(fname):
    paths = read_input(fname, types=[str])
    return Maze(paths)


##########
# PART 1 #
##########


@cached({}, key=lambda m, p, v: hashkey(tuple(p), frozenset(v)))
def traverse(maze: Maze, path: List[str], visited: Set[str]) -> Set[Tuple[str]]:
    current_cave_name = path[-1]
    if current_cave_name == 'end':
        return frozenset({tuple(path)})

    paths_to_end = set()

    for cave in maze.outgoing_caves(current_cave_name):
        if cave.name not in visited or cave.big:
            paths_to_end |= traverse(maze, path + [cave.name], visited | {cave.name})

    return frozenset(paths_to_end)


def part_one():
    maze = parse(fname)
    start_path = ['start']
    paths_to_end = traverse(maze, start_path, set(start_path))
    return len(paths_to_end)


##########
# PART 2 #
##########


@cached({}, key=lambda m, p, v, db_sm: hashkey(tuple(p), frozenset(v), db_sm))
def traverse_p2(maze: Maze, path: List[str], visited: Set[str], used_double_small: bool) -> Set[Tuple[str]]:
    current_cave_name = path[-1]
    if current_cave_name == 'end':
        return frozenset({tuple(path)})

    paths_to_end = set()

    for cave in maze.outgoing_caves(current_cave_name):
        if cave.name not in visited or cave.big:
            paths_to_end |= traverse_p2(maze, path + [cave.name], visited | {cave.name}, used_double_small)
        elif not used_double_small and cave.name != 'start':
            paths_to_end |= traverse_p2(maze, path + [cave.name], visited | {cave.name}, True)

    return frozenset(paths_to_end)



def part_two():
    maze = parse(fname)
    start_path = ['start']
    paths_to_end = traverse_p2(maze, start_path, set(start_path), False)
    return len(paths_to_end)


if __name__ == '__main__':
    print("Part 1")
    print(part_one())
    print("Part 2")
    print(part_two())
