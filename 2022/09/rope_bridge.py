from utils import read_input, run
import numpy as np


FNAME = "09/input.txt"

UP = np.array([0, 1])
DOWN = np.array([0, -1])
LEFT = np.array([-1, 0])
RIGHT = np.array([1, 0])


def parse_line(line):
    split = line.split(' ')
    return split[0], int(split[1])


##########
# PART 1 #
##########


def direction_vector(direction):
    if direction == 'U':
        return UP
    elif direction == 'D':
        return DOWN
    elif direction == 'L':
        return LEFT
    elif direction == 'R':
        return RIGHT
    raise Exception('Unknown direction')


def move_head(head, dir):
    return head + direction_vector(dir)


def move_tail(tail, head):
    diff = head - tail
    if any(abs(diff) > 1):
        return tail + np.clip(diff, -1, 1)
    return tail


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    head = np.array([0, 0])
    tail = np.array([0, 0])
    visited = {(0, 0)}
    
    for direction, repeats in data:
        for _ in range(repeats):
            head = move_head(head, direction)
            tail = move_tail(tail, head)

            visited.add(tuple(tail))
    
    return len(visited)


##########
# PART 2 #
##########


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    rope = [np.array([0, 0]) for _ in range(10)]
    visited = {(0, 0)}
    
    for direction, repeats in data:
        for _ in range(repeats):
            rope[0] = move_head(rope[0], direction)
            for i in range(1, len(rope)):
                rope[i] = move_tail(rope[i], rope[i-1])

            visited.add(tuple(rope[-1]))
    
    return len(visited)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
