from typing import Optional
from utils import read_input, run
from json import loads
from dataclasses import dataclass


fname = "day18/input.txt"


def parse(fname):
    return [loads(line) for line in read_input(fname, types=[str])]



class Node:
    def __init__(self, data, parent: Optional['Node'] = None) -> None:
        self.parent = parent
        if isinstance(data, int):
            self.value = data
            self.left = None
            self.right = None
        elif isinstance(data, list):
            left_data, right_data = data
            self.value = None
            self.left = Node(left_data)
            self.right = Node(right_data)

    def is_top(self) -> bool:
        return self.parent is None
    
    def is_regular_number(self) -> bool:
        return self.value is not None

    def is_left(self) -> bool:
        return not self.is_top() and self.parent.left is self
    
    def is_right(self) -> bool:
        return not self.is_top() and self.parent.right is self

    def explode(self) -> None:
        pass

    def split(self) -> None:
        if self.is_regular_number():
            pass
    
    def __repr__(self) -> str:
        if self.is_regular_number():
            return repr(self.value)
        else:
            return repr([self.left, self.right])




##########
# PART 1 #
##########


def snail_add(n1, n2):
    result = [n1, n2]


def part_one():
    data = parse(fname)
    tree = Node(data)
    print(tree)


##########
# PART 2 #
##########


def part_two():
    pass


if __name__ == '__main__':
    run(part_one, part_two)
