import sys
import numpy as np
from utils import read_input, run
from functools import cache
from collections import deque


FNAME = "24/input.txt"
E = (0, 1)
S = (1, 0)
W = (0, -1)
N = (-1, 0)
BLIZZARD = 1
DIRECTIONS = {
    '>': E,
    'v': S,
    '<': W,
    '^': N,
}
MAX_SEARCH_DEPTH = 300
sys.setrecursionlimit(MAX_SEARCH_DEPTH * 5)


def parse_input(input_file):
    data = read_input(input_file, parse_chunk=lambda l: l[1:len(l)-1])
    data = data[1:len(data)-1]
    grid = np.zeros((len(data), len(data[0])))

    blizzards = []

    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if char == '#':
                raise Exception('Found wall')
            elif char in DIRECTIONS:
                blizzards.append(((i, j), DIRECTIONS[char]))

    return grid, blizzards


##########
# PART 1 #
##########


def add(c1, c2):
    return tuple(a + b for a, b in zip(c1, c2))


def wrap(coord, grid):
    return tuple(a % grid.shape[i] for i, a in enumerate(coord))


def possible_moves(next_grid, pos):
    return list(filter(lambda p: in_start_end(p, next_grid) or in_grid(p, next_grid) and not next_grid[p], (add(pos, d) for d in (E, S, W, N, (0, 0)))))


def in_start_end(pos, grid):
    return pos == (-1, 0) or pos == add(grid.shape, W)


def in_grid(pos, grid):
    return all(0 <= pos[i] < grid.shape[i] for i in range(2))


def move_blizzard(grid, blizzard):
    pos, direction = blizzard
    return wrap(add(pos, direction), grid), direction


def part_one(input_file):
    empty_grid, blizzards = parse_input(input_file)
    start = (0, 0)
    goal = (empty_grid.shape[0] - 1, empty_grid.shape[1] - 1)
    best = MAX_SEARCH_DEPTH
    
    @cache
    def blizzards_after(mins):
        if mins < 0:
            raise Exception()
        if mins == 0:
            return blizzards
        return [move_blizzard(empty_grid, b) for b in blizzards_after(mins - 1)]

    @cache
    def grid_after(mins):
        grid = np.zeros(empty_grid.shape)
        for coord, _ in blizzards_after(mins):
            grid[coord] = BLIZZARD
        return grid

    @cache
    def shortest_path(pos, mins):
        nonlocal best 
        if mins >= best:
            return np.inf
        if pos == goal:
            return 1
        grid = grid_after(mins + 1)
        moves = possible_moves(grid, pos)
        res = 1 + min((shortest_path(m, mins + 1) for m in moves), default=np.inf)
        if pos == start and res + mins < best:
            best = res + mins
            print(f"{best=}")
        return res

    return shortest_path(start, 0)


##########
# PART 2 #
##########


def part_two(input_file):
    empty_grid, blizzards = parse_input(input_file)
    start = (-1, 0)
    end = (empty_grid.shape[0] - 1, empty_grid.shape[1] - 1)
    
    @cache
    def blizzards_after(mins):
        if mins < 0:
            raise Exception()
        if mins == 0:
            return blizzards
        return [move_blizzard(empty_grid, b) for b in blizzards_after(mins - 1)]

    @cache
    def grid_after(mins):
        grid = np.zeros(empty_grid.shape)
        for coord, _ in blizzards_after(mins):
            grid[coord] = BLIZZARD
        return grid

    def find_shortest_path(start, end, mins):
        best = MAX_SEARCH_DEPTH + mins
        print(f"Starting {start=} to {end=}")

        @cache
        def shortest_path(pos, goal, mins):
            nonlocal best 
            if mins >= best:
                return np.inf
            if pos == goal:
                return 1
            grid = grid_after(mins + 1)
            moves = possible_moves(grid, pos)
            res = 1 + min((shortest_path(m, goal, mins + 1) for m in moves), default=np.inf)
            if pos == start and res + mins < best:
                best = res + mins
                print(f"{best=}")
            return res
        
        return mins + shortest_path(start, end, mins)

    return find_shortest_path(start, end, find_shortest_path(end, start, find_shortest_path(start, end, 0)))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
