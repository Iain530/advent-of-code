from utils import read_input, run
import numpy as np
from typing import Callable


FNAME = "13/input.txt"

def parse_paragraph(para: str) -> np.ndarray:
    return np.array([
        list(line) for line in para.split('\n')
    ])


##########
# PART 1 #
##########



def reflect_horizontally(array: np.ndarray, col: int) -> tuple[np.ndarray, np.ndarray]:
    size = min(col, array.shape[1] - col)
    left = np.flip(array[:,:col], axis=1)
    right = array[:,col:]

    left = left[:,:size]
    right = right[:,:size]
    
    return left, right


def reflect_vertically(array: np.ndarray, row: int) -> tuple[np.ndarray, np.ndarray]:
    size = min(row, array.shape[0] - row)
    top = np.flip(array[:row,:], axis=0)
    bottom = array[row:,:]

    top = top[:size,:]
    bottom = bottom[:size,:]

    return top, bottom


def summary_score(array: np.ndarray, condition: Callable[[np.ndarray, np.ndarray], bool]) -> int:
    for col in range(1, array.shape[1]):
        l, r = reflect_horizontally(array, col)
        if condition(l, r):
            return col
    for row in range(1, array.shape[0]):
        t, b = reflect_vertically(array, row)
        if condition(t, b):
            return row * 100

    raise Exception('No reflection found')


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_paragraph, separator='\n\n')
    return sum(summary_score(array, lambda a, b: np.all(a == b)) for array in data)


##########
# PART 2 #
##########


def is_one_off_reflection(a, b) -> bool:
    return len(list((filter(bool, (a != b).flatten())))) == 1


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_paragraph, separator='\n\n')
    return sum(summary_score(array, is_one_off_reflection) for array in data)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
