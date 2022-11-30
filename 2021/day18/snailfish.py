from typing import Optional
from utils import read_input, run
from json import loads
from math import floor, ceil
from functools import cached_property
from itertools import permutations


fname = "day18/input.txt"


def parse(fname):
    return [Node(loads(line)) for line in read_input(fname, types=[str])]


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
            self.left = Node(left_data, self)
            self.right = Node(right_data, self)

    @cached_property
    def depth(self) -> int:
        d = 0
        current = self
        while not current.is_top():
            current = current.parent
            d += 1
        return d

    def is_top(self) -> bool:
        return self.parent is None
    
    def is_regular_number(self) -> bool:
        return self.value is not None

    def is_left(self) -> bool:
        return not self.is_top() and self.parent.left is self
    
    def is_right(self) -> bool:
        return not self.is_top() and self.parent.right is self
    
    def reduce(self) -> None:
        while (node := self.find_next_invalid()):
            if node.is_regular_number():
                node.split()
            else:
                node.explode()
    
    def find_next_invalid(self) -> Optional['Node']:
        for node in self:
            if not node.is_regular_number() and node.depth >= 4:
                return node
        for node in self:
            if node.is_regular_number() and node.value >= 10:
                return node
        return None
    
    def is_tree_valid(self) -> bool:
        return all(node.is_node_valid() for node in self)
    
    def is_node_valid(self) -> bool:
        if self.is_regular_number():
            return self.value < 10
        else:
            return self.depth < 4  
    
    def magnitude(self) -> int:
        if self.is_regular_number():
            return self.value
        
        left_mag = self.left.magnitude()
        right_mag = self.right.magnitude()
        return left_mag * 3 + right_mag * 2

    def explode(self) -> None:
        assert self.left.is_regular_number()
        assert self.right.is_regular_number()
        
        l_node = self.next_left_regular_number()
        if l_node:
            l_node.value += self.left.value
        
        r_node = self.next_right_regular_number()
        if r_node:
            r_node.value += self.right.value
        
        self.value = 0
        self.left = None
        self.right = None

    def next_left_regular_number(self):      
        current = self
        # Traverse up until can go left
        while current.is_left():
            current = current.parent
        # If reached the top then we're in the leftmost node already (discard)
        if current.is_top():
            return None
        # Hop left one step
        current = current.parent.left
        # Traverse down right to find the adjacent node
        while not current.is_regular_number():
            current = current.right
        return current

    def next_right_regular_number(self):        
        current = self
        # Traverse up until can go right
        while current.is_right():
            current = current.parent
        # If reached the top then we're in the rightmost node already (discard)
        if current.is_top():
            return None
        # Hop right one step
        current = current.parent.right
        # Traverse down left to find the adjacent node
        while not current.is_regular_number():
            current = current.left
        return current

    def split(self) -> None:
        if self.is_regular_number():
            half = self.value / 2
            left = floor(half)
            right = ceil(half)
            self.left = Node(left, self)
            self.right = Node(right, self)
            self.value = None
    
    def to_primitive(self):
        if self.is_regular_number():
            return self.value
        else:
            return [
                self.left.to_primitive(),
                self.right.to_primitive(),
            ]

    def __add__(self, other) -> 'Node':
        if not isinstance(other, Node):
            raise NotImplementedError()
        left = self.to_primitive()
        right = other.to_primitive()
        result = Node([left, right])
        result.reduce()
        return result
    
    def __radd__(self, other) -> 'Node':
        if other == 0:
            return self
        raise NotImplementedError()   

    def __iter__(self):
        yield self
        if not self.is_regular_number():
            yield from iter(self.left)
            yield from iter(self.right)
    
    def __repr__(self) -> str:
        return repr(self.to_primitive())


##########
# PART 1 #
##########


def part_one():
    snail_numbers = parse(fname)
    return sum(snail_numbers).magnitude()


##########
# PART 2 #
##########


def part_two():
    snail_numbers = parse(fname)
    result = max(sum(pair).magnitude() for pair in permutations(snail_numbers, 2))
    return result


if __name__ == '__main__':
    run(part_one, part_two)
