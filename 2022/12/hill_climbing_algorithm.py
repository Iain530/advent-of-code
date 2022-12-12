import numpy as np
from utils import read_input, run

FNAME = "12/input.txt"


def create_grid(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            letter = data[i][j]
            if letter == 'S':
                start = (i, j)
                data[i][j] = 1
            elif letter == 'E':
                end = (i, j)
                data[i][j] = 26
            else:
                data[i][j] = ord(letter) - 96
    return np.array(data), start, end
    

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

    return [p for p in possible if grid[p] - grid[coord] <= 1]


def dijkstra(grid, start, end, default=np.inf):
    distances = np.full(grid.shape, np.inf)
    distances[start] = 0
    unvisited = {start}
    visited = set()

    current = start
    while current != end:

        for neighbour in find_possible_steps(grid, current):
            if neighbour not in visited:
                dist = distances[current] + 1
                if dist < distances[neighbour]:
                    distances[neighbour] = dist
                unvisited.add(neighbour)
        
        visited.add(current)
        unvisited.remove(current)
        if len(unvisited) == 0:
            return default
        current = min(unvisited, key=lambda u: distances[u])

    return int(distances[end])


def part_one(input_file):
    grid, start, end = create_grid(read_input(input_file, parse_chunk=lambda l: list(l)))
    return dijkstra(grid, start, end)


##########
# PART 2 #
##########


def part_two(input_file):
    grid, _, end = create_grid(read_input(input_file, parse_chunk=lambda l: list(l)))
    return min(dijkstra(grid, (x, y), end) for x in range(len(grid)) for y in range(len(grid[x])) if grid[(x, y)] == 1)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
