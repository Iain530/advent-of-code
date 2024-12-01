from utils import read_input, run
import numpy as np


FNAME = "21/input.txt"


##########
# PART 1 #
##########


def find_possible_steps(grid, coord):
    x, y = coord
    possible = []
    if x > 0:
        possible.append((x-1, y))
    if y > 0:
        possible.append((x, y-1))
    if x < len(grid) - 1:
        possible.append((x+1, y))
    if y < len(grid[x]) - 1:
        possible.append((x, y+1))

    return [p for p in possible if grid[p] == '.']



def dijkstra(grid, start, default=np.inf):
    distances = np.full(grid.shape, np.inf)
    distances[start] = 0
    unvisited = {start}
    visited = set()

    current = start
    while unvisited:
        for neighbour in find_possible_steps(grid, current):
            if neighbour not in visited:
                dist = distances[current] + 1
                if dist < distances[neighbour]:
                    distances[neighbour] = dist
                unvisited.add(neighbour)
        
        visited.add(current)
        unvisited.remove(current)
        if len(unvisited) == 0:
            break
        current = min(unvisited, key=lambda u: distances[u])

    return len(list(filter(bool, ((distances <= 64) & (distances % 2 == 0)).flatten())))


def find_and_replace_start(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            coord = (i, j)
            if grid[coord] == 'S':
                grid[coord] = '.'
                return coord


def part_one(input_file):
    grid = np.array(read_input(input_file, parse_chunk=list))
    start = find_and_replace_start(grid)
    return dijkstra(grid, start)




##########
# PART 2 #
##########


def part_two(input_file):
    pass


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
