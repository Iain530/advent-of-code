from utils import read_input, run, UP, DOWN, LEFT, RIGHT, DIRECTIONS, Vector, add, iter_grid
import numpy as np
import sys
from collections import defaultdict
from heapq import heapify, heappop, heappush
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class State:
    score: int
    steps: tuple[Vector, Vector, set[Vector]]=field(compare=False)


sys.setrecursionlimit(100000)

FNAME = "16/input.txt"
Grid = np.ndarray

def parse_input(input_file):
    pass

##########
# PART 1 #
##########



def find_start(grid: Grid) -> Vector:
    for position in iter_grid(grid):
        if grid[position] == 'S':
            return position


ROTATIONS = {
    LEFT: [UP, DOWN],
    RIGHT: [UP, DOWN],
    UP: [RIGHT, LEFT],
    DOWN: [RIGHT, LEFT],
}

def show(path):
    grid = np.array(read_input(FNAME, parse_chunk=list))
    for p in path:
        grid[p] = 'o'
    for line in grid:
        print(''.join(line))

def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    start = find_start(grid)
    cache = defaultdict(lambda: np.inf)

    def can_move(position, direction, path) -> bool:
        next_pos = add(position, direction)
        return grid[next_pos] != '#' and next_pos not in path

    def find_next_steps(position: Vector, direction: Vector, path: set):
        for next_direction in [direction, *ROTATIONS[direction]]:
            if can_move(position, next_direction, path):
                yield (1 if next_direction == direction else 1001), (add(position, next_direction), next_direction, path | {position})
    
    def key(state: State):
        position, direction, _path = state.steps
        return position, direction

    queue = [State(0, (start, RIGHT, set()))]
    heapify(queue)

    while (state := heappop(queue)):
        position, direction, path = state.steps

        if grid[position] == 'E':
            return state.score
    
        if state.score >= cache[key(state)]:
            continue

        cache[key(state)] = state.score
    
        for score, steps in find_next_steps(position, direction, path):
            heappush(queue, State(state.score + score, steps))



##########
# PART 2 #
##########


def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    start = find_start(grid)
    cache = defaultdict(lambda: np.inf)
    best_path_tiles = set()
    best_score = None

    def can_move(position, direction, path) -> bool:
        next_pos = add(position, direction)
        return grid[next_pos] != '#' and next_pos not in path

    def find_next_steps(position: Vector, direction: Vector, path: set):
        for next_direction in [direction, *ROTATIONS[direction]]:
            if can_move(position, next_direction, path):
                yield (1 if next_direction == direction else 1001), (add(position, next_direction), next_direction, path | {position})
    
    def key(state: State):
        position, direction, _path = state.steps
        return position, direction

    queue = [State(0, (start, RIGHT, set()))]
    heapify(queue)

    while queue:
        state = heappop(queue)
        position, direction, path = state.steps

        if grid[position] == 'E' and (best_score is None or state.score == best_score):
            best_path_tiles |= path | {position}
            best_score = state.score
            continue

        if state.score > cache[key(state)]:
            continue

        cache[key(state)] = state.score
    
        for score, steps in find_next_steps(position, direction, path):
            heappush(queue, State(state.score + score, steps))

    show(best_path_tiles)
    return len(best_path_tiles)

if __name__ == '__main__':
    run(part_one, part_two, FNAME)
