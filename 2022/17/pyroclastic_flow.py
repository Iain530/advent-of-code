import numpy as np
from utils import read_input, run
import matplotlib.pyplot as plt
from matplotlib import animation


FNAME = "17/input.txt"


def horizontal_shape(height):
    return [(i, height) for i in range(2, 6)]


def plus_shape(height):
    return [
        (3, height),
        (2, height + 1),
        (3, height + 1),
        (4, height + 1),
        (3, height + 2),
    ]


def corner_shape(height):
    return [
        (2, height),
        (3, height),
        (4, height),
        (4, height + 1),
        (4, height + 2),
    ]


def vertical_shape(height):
    return [(2, height + i) for i in range(4)]


def square_shape(height):
    return [
        (2, height),
        (2, height + 1),
        (3, height),
        (3, height + 1),
    ]


def all_shapes(height):
    order = [
        horizontal_shape,
        plus_shape,
        corner_shape,
        vertical_shape,
        square_shape,
    ]
    i = 0
    while True:
        height = yield order[i](height)
        i = (i + 1) % len(order)


DIRECTIONS = {
    '>': 1,
    '<': -1
}


def move(grid, shape, direction):
    new_shape = [(x + direction, y) for x, y in shape]
    if any(x < 0 or x > 6 or grid[(x, y)] for x, y in new_shape):
        return shape
    return new_shape


def drop(grid, shape):
    new_shape = [(x, y - 1) for x, y in shape]
    if any(grid[coord] for coord in new_shape):
        return shape, False
    return new_shape, True


##########
# PART 1 #
##########


def part_one(input_file):
    data = read_input(input_file, parse_chunk=lambda l: [DIRECTIONS[a] for a in l])[0]
    grid = np.zeros((7, 5000))
    grid[:, 0] = 1
    heights = [0] * 7

    gen_shapes = all_shapes(4)
    shape = next(gen_shapes)
    directions = iter(data * 2)


    for i in range(2022):
        if not shape:
            shape = gen_shapes.send(max(heights) + 4)
        while shape:
            direction = next(directions)

            shape = move(grid, shape, direction)
            shape, moved = drop(grid, shape)

            if not moved:
                for x, y in shape:
                    grid[(x, y)] = (i % 5) + 1
                    heights[x] = max(heights[x], y)
                shape = None

    return max(heights)


##########
# PART 2 #
##########


def part_two(input_file):
    data = read_input(input_file, parse_chunk=lambda l: [DIRECTIONS[a] for a in l])[0]
    grid = np.zeros((7, 10000000))
    grid[:, 0] = 1
    heights = [0] * 7

    gen_shapes = all_shapes(4)
    shape = next(gen_shapes)
    directions = iter(data * 2)

    moves = 0

    for i in range(1000000000000):
        if not shape:
            shape = gen_shapes.send(max(heights) + 4)
        while shape:
            direction = next(directions)
            moves += 1

            shape = move(grid, shape, direction)
            shape, moved = drop(grid, shape)

            if not moved:
                for x, y in shape:
                    grid[(x, y)] = (i % 5) + 1
                    heights[x] = max(heights[x], y)
                shape = None
            
            if moves % len(data) == 0:
                directions = iter(data)
                if shape is None:
                    print('Maybe')

                if shape is None and i % 5 == 0:
                    print(heights)
                    print(grid[:, max(heights)-5:max(heights)+2])
                    print(moves)
                    print(i)
                    return

    
    return max(heights)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
