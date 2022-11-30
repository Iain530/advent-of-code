from itertools import tee
from utils import read_input


def sliding_window(iterable, size):
    iterables = tee(iterable, size)
    for i, iterator in enumerate(iterables):
        for _ in range(i):
            next(iterator)
    return zip(*iterables)


if __name__ == "__main__":
    depths = read_input('day1/input.txt', types=[int])

    increases = 0
    current, *windows = sliding_window(depths, 3)
    for window in windows:
        if sum(window) > sum(current):
            increases += 1
        current = window

    print(increases)
