import numpy as np


fname = "day13/input.txt"


def read_input(fname):
    with open(fname) as f:
        point_lines, fold_lines = f.read().split('\n\n')
    
    points = [tuple(int(p) for p in point.split(',')) for point in point_lines.split('\n')]
    folds = []
    for fold in fold_lines.strip().split('\n'):
        axis, value = fold.split()[-1].split('=')
        folds.append((axis, int(value)))
    return points, folds

##########
# PART 1 #
##########


def grid_size(folds):
    x = max(f[1] for f in folds if f[0] == 'x')
    y = max(f[1] for f in folds if f[0] == 'y')
    return y*2 + 1, x*2 + 1


def mark_points(grid, points):
    for x, y in points:
        grid[y][x] = 1


def fold(grid, axis):
    mid = grid.shape[axis] // 2
    grid = np.delete(grid, mid, axis=axis)
    base, fold = np.split(grid, 2, axis=axis)
    flipped = np.flip(fold, axis=axis)
    base[flipped == 1] = 1
    return base


def visible_dots(grid):
    return np.count_nonzero(grid == 1)


def part_one():
    points, folds = read_input(fname)
    size = grid_size(folds)
    grid = np.zeros(size)
    
    mark_points(grid, points)

    for dir, _ in folds:
        axis = 1 if dir == 'x' else 0
        grid = fold(grid, axis)
        break  # Do first only

    return visible_dots(grid)

##########
# PART 2 #
##########


def visualize(grid):
    for row in grid:
        for cell in row:
            if cell == 1:
                print('#', end='')
            else:
                print(' ', end='')
        print()


def part_two():
    points, folds = read_input(fname)
    size = grid_size(folds)
    grid = np.zeros(size)
    
    mark_points(grid, points)

    for dir, _ in folds:
        axis = 1 if dir == 'x' else 0
        grid = fold(grid, axis)

    visualize(grid)


if __name__ == '__main__':
    print("Part 1")
    print(part_one())
    print("Part 2")
    part_two()
