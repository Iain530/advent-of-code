from utils import read_input, run, Vector, add
from collections import defaultdict
from functools import reduce
from operator import mul
import statistics
import numpy as np
import time
import sys
import math

np.set_printoptions(threshold=sys.maxsize)


FNAME = "14/input.txt"


def parse_line(line: str) -> list[Vector]:
    return [tuple(map(int, pv.lstrip('pv=').split(','))) for pv in line.split()]


##########
# PART 1 #
##########


X_SIZE = 101
Y_SIZE = 103

MIDDLE_X = X_SIZE // 2
MIDDLE_Y = Y_SIZE // 2


def safety_factor(robots) -> int:
    quadrants = defaultdict(int)
    for position, _ in robots:
        x, y = position
        if x == MIDDLE_X or y == MIDDLE_Y:
            continue

        quadrants[(int(x > MIDDLE_X), int(y > MIDDLE_Y))] += 1
    
    return reduce(mul, quadrants.values(), 1)


def step(robot: tuple[Vector, Vector]) -> Vector:
    position, velocity = robot
    x, y = add(position, velocity)
    return (x % X_SIZE, y % Y_SIZE), velocity


def part_one(input_file):
    robots = read_input(input_file, parse_chunk=parse_line)

    for _ in range(100):
        robots = list(map(step, robots))
    
    return safety_factor(robots)
        


##########
# PART 2 #
##########

def show(robots, i):
    grid = np.zeros((X_SIZE, Y_SIZE), dtype=str)
    grid[:,:] = ' '
    for pos, _ in robots:
        grid[pos] = '^'
    
    for line in grid:
        for ch in line:
            print(ch, end='')
        print('')
    print(str(i) + '-' * 100)



def part_two(input_file):
    robots = read_input(input_file, parse_chunk=parse_line)
    
    safetys = []
    for i in range(10000):
        robots = list(map(step, robots))
        safetys.append(safety_factor(robots))
        if i > 2:
            mean = statistics.mean(safetys)
            stdev = statistics.stdev(safetys)

            if abs(safetys[-1] - mean) > stdev:
                show(robots, i + 1)
                time.sleep(0.2)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
