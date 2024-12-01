from utils import read_input, run
import numpy as np
import sys

sys.setrecursionlimit(20000)


FNAME = "23/input.txt"


##########
# PART 1 #
##########


def find_path(grid, x=0):
    return next((x, i) for i in range(grid.shape[1]) if grid[x,i] != '#')


def find_possible_steps(grid, coord, part_two=False):
    x, y = coord
    if not part_two:
        if grid[coord] == '>':
            return [(x, y+1)]
        if grid[coord] == 'v':
            return [(x+1, y)]
        if grid[coord] == '<':
            return [(x, y-1)]
        if grid[coord] == '^':
            return [(x-1, y)]
    
    possible = []
    if x > 0:
        possible.append((x-1, y))
    if y > 0:
        possible.append((x, y-1))
    if x < len(grid) - 1:
        possible.append((x+1, y))
    if y < len(grid[x]) - 1:
        possible.append((x, y+1))

    return [p for p in possible if grid[p] != '#']


def show(grid):
    print('\n'.join(''.join(line) for line in grid))


def find_longest_hike(grid, current, end, path, part_two=False):
    if current == end:
        print(f'Found end with length {len(path)}')
        return len(path)
    
    new_path = path | {current}

    return max((find_longest_hike(grid, neighbour, end, new_path, part_two=part_two) for neighbour in find_possible_steps(grid, current, part_two=part_two) if neighbour not in new_path), default=0)



def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    start = find_path(grid)
    end = find_path(grid, grid.shape[0] - 1)
    return find_longest_hike(grid, start, end, set())


##########
# PART 2 #
##########



def part_two(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    start = find_path(grid)
    end = find_path(grid, grid.shape[0] - 1)
    return find_longest_hike(grid, start, end, set(), part_two=True)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
