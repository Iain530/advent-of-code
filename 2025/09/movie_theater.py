from utils import read_input, run, add, UP, DOWN, LEFT, RIGHT
from itertools import permutations, pairwise
from collections import deque


FNAME = "09/input.txt"

Point = tuple[int, int]


def parse_line(line: str) -> Point:
    return tuple(map(int, line.split(',')))


##########
# PART 1 #
##########


def area(p1: Point, p2: Point) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)


def part_one(input_file):
    points = read_input(input_file, parse_chunk=parse_line)
    return max(area(p1, p2) for p1, p2 in permutations(points, 2))


##########
# PART 2 #
##########


def shrink(points: list[Point], axis: int) -> dict[int, int]:
    axis_points = sorted(set(p[axis] for p in points))
    sizes = {}
    for i, p in enumerate(axis_points):
        sizes[p] = i

    return sizes


def show(grid):
    result = '\n'.join(map(''.join, grid))
    with open('output.txt', 'w+') as f:
        f.write(result)


def draw_point(grid, point):
    x, y = point
    grid[y][x] = '#'


def draw_line(grid, p1: Point, p2: Point):
    x1, y1 = p1
    x2, y2 = p2
    
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2)):
            grid[y][x1] = 'X'

    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2)):
            grid[y1][x] = 'X'


def is_in_grid(grid, point: Point):
    x, y = point
    if x < 0 or y < 0:
        return False
    if y > len(grid) or x > len(grid[0]):
        return False
    return True


def flood_fill(grid, origin: Point, find: str, replace: str):
    queue = deque()
    queue.append(origin)

    while queue:
        point = queue.popleft()
        x, y = point
        value = grid[y][x]
        if value != find:
            continue
        
        grid[y][x] = replace

        neighbours = filter(lambda p: is_in_grid(grid, p), (add(point, d) for d in (UP, DOWN, LEFT, RIGHT)))
        for n in neighbours:
            queue.append(n)


def is_valid(p1, p2, grid):
    x1, y1 = p1
    x2, y2 = p2

    for x in range(min(x1, x2), max(x1, x2) + 1):
        if any(grid[y][x] == '.' for y in (y1, y2)):
            return False
    
    for y in range(min(y1, y2), max(y1, y2) + 1):
        if any(grid[y][x] == '.' for x in (x1, x2)):
            return False
    
    return True


def draw_rect(p1, p2, grid, value='O'):
    x1, y1 = p1
    x2, y2 = p2

    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in (y1, y2):
            grid[y][x] = value
    
    for y in range(min(y1, y2), max(y1, y2) + 1):
        for x in (x1, x2):
            grid[y][x] = value


def part_two(input_file):
    points = read_input(input_file, parse_chunk=parse_line)

    x_sizes = shrink(points, 0)
    y_sizes = shrink(points, 1)
    x_reverse_index = {v: k for k,v in x_sizes.items()}
    y_reverse_index = {v: k for k,v in y_sizes.items()}


    def to_shrunk_point(point: Point) -> Point:
        x, y = point
        return (x_sizes[x], y_sizes[y])

    def grow_point(point: Point) -> Point:
        x, y = point
        return (x_reverse_index[x], y_reverse_index[y])

    for p in points:
        assert p == grow_point(to_shrunk_point(p))

    shrunk_points = list(map(to_shrunk_point, points))
    
    grid = [['.' for i in range(len(x_sizes))] for j in range(len(y_sizes))]

    for p1, p2 in pairwise(shrunk_points):
        draw_line(grid, p1, p2)
        draw_point(grid, p1)
    draw_line(grid, shrunk_points[-1], shrunk_points[0])
    draw_point(grid, shrunk_points[-1])
    draw_point(grid, shrunk_points[0])

    flood_fill(grid, (100, 100), '.', 'X')

    return max(area(grow_point(p1), grow_point(p2)) for p1, p2 in permutations(shrunk_points, 2) if is_valid(p1, p2, grid))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
