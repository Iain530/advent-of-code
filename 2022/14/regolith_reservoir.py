import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from utils import read_input, run, sliding_window


FNAME = "14/input.txt"
WALL = 1
SAND = 2

def parse_chunk(line):
    return [tuple(map(int, coord.split(','))) for coord in line.split(' -> ')]


##########
# PART 1 #
##########


def line_points(start, end):
    x1, y1 = start
    x2, y2 = end
    if x1 == x2:
        return [(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)]
    elif y1 == y2:
        return [(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)]


def build_grid(lines):
    max_y = max(y for l in lines for _, y in l) + 3
    grid = np.zeros((1001, max_y))

    for line in lines:
        for start, end in sliding_window(line, 2):
            for point in line_points(start, end):
                grid[point] = WALL

    return grid


def try_move(grid, sand):
    x, y = sand
    next_y = y + 1
    if x == 0:
        raise Exception(f'{sand}')
    if not grid[(x, next_y)]:
        return (x, next_y)
    if not grid[(x-1, next_y)]:
        return (x-1, next_y)
    if not grid[(x+1, next_y)]:
        return (x+1, next_y)
    
    return sand


def simulate_sand(grid):
    current = (500, 0)
    if grid[current]:
        return False  # Full

    while True:
        next_position = try_move(grid, current)
        if next_position == current:
            grid[current] = SAND
            return True  # Landed
        
        if next_position[1] == grid.shape[1] - 1:
            return False  # Abyss

        current = next_position


def part_one(input_file):
    grid = build_grid(read_input(input_file, parse_chunk=parse_chunk))

    landed = 0
    while simulate_sand(grid):
        landed += 1

    # def next_grid():
    #     simulate_sand(grid)
    #     return grid
    
    # show(grid, frames=862, next_grid=next_grid)
    
    return landed
    



##########
# PART 2 #
##########


def part_two(input_file):
    grid = build_grid(read_input(input_file, parse_chunk=parse_chunk))
    grid[:, grid.shape[1] - 1] = WALL

    landed = 0
    while simulate_sand(grid):
        landed += 1
    
    # def next_grid():
    #     for i in range(30):
    #         simulate_sand(grid)
    #     return grid

    # show(grid, frames=925, next_grid=next_grid)

    return landed


def show(grid, frames, next_grid):
    def format(grid):
        return grid.T[:,350:650]

    fig = plt.figure()
    im = plt.imshow(format(grid), animated=True, cmap='viridis', vmin=0, vmax=2)
    plt.tight_layout()
    plt.grid(False)
    plt.axis('off')

    def init():
        im.set_data(format(grid))
        return im,

    def animate(i):
        im.set_array(format(next_grid()))
        return im,

    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        frames=frames,
        interval=1,
        blit=True,
    )

    anim.save(f"sand_{frames}.gif")
    plt.show()


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
