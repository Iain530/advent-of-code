from utils import read_input
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple
from itertools import permutations

fname = "day12/input.txt"

START = 'start'
END = 'end'

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


def traverse(maze: Maze, path: List[str], visited: Set[str]) -> List[List[str]]:
    current_cave_name = path[-1]
    if current_cave_name == END:
        return [path]

    paths_to_end = list()

    for cave in maze.outgoing_caves(current_cave_name):
        if cave.name not in visited or cave.big:
            paths_to_end += traverse(maze, path + [cave.name], visited | {cave.name})

    return paths_to_end


def part_one():
    maze = parse(fname)
    paths_to_end = traverse(maze, [START], {START})
    return len(paths_to_end)


##########
# PART 2 #
##########


def traverse_part_2(maze: Maze, path: List[str], visited: Set[str], visited_small_twice: bool) -> List[List[str]]:
    current_cave_name = path[-1]
    if current_cave_name == END:
        return [path]

    paths_to_end = list()

    for cave in maze.outgoing_caves(current_cave_name):
        if cave.name not in visited or cave.big:
            paths_to_end += traverse_part_2(maze, path + [cave.name], visited | {cave.name}, visited_small_twice)
        elif not visited_small_twice and cave.name != START:
            paths_to_end += traverse_part_2(maze, path + [cave.name], visited | {cave.name}, True)

    return paths_to_end



def part_two():
    maze = parse(fname)
    paths_to_end = traverse_part_2(maze, [START], {START}, False)
    return len(paths_to_end)


if __name__ == '__main__':
    run(part_one, part_two)
