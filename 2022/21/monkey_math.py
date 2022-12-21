from utils import read_input, run
from operator import mul, add, sub, truediv, eq
from functools import cache, cached_property
from dataclasses import dataclass
from typing import Callable, Optional


FNAME = "21/input.txt"


def parse_line(line):
    label, *value = line.split(' ')
    label = label.rstrip(':')
    if len(value) == 1:
        value = int(value[0])
    else:
        operator = OPERATIONS[value[1]]
        value = (operator, value[0], value[2])

    return label, value


##########
# PART 1 #
##########


OPERATIONS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}


def build_variables(data):
    return {label: value for label, value in data}
        

def part_one(input_file):
    variables = build_variables(read_input(input_file, parse_chunk=parse_line))

    @cache
    def get_value(label):
        val = variables[label]
        if isinstance(val, int):
            return val
        
        operator, a, b = val
        return int(operator(get_value(a), get_value(b)))

    return get_value('root')


##########
# PART 2 #
##########


@dataclass
class Node:
    name: str
    value: Optional[int] = None
    op: Callable[[int, int], int] = None
    left: Optional['Node'] = None
    right: Optional['Node'] = None

    @cached_property
    def is_known(self) -> bool:
        return self.value is not None or (self.has_children() and self.left.is_known and self.right.is_known)
    
    def has_children(self) -> bool:
        return self.left is not None and self.right is not None

    def simplify(self) -> Optional[int]:
        if self.is_known and self.value is None:
            self.value = int(self.op(self.left.simplify(), self.right.simplify()))
            self.left = None
            self.right = None
            self.op = None
        elif self.has_children():
            self.left.simplify()
            self.right.simplify()
        return self.value
    
    def get_children(self) -> tuple['Node', 'Node']:
        return self.left, self.right


def part_two(input_file):
    variables = build_variables(read_input(input_file, parse_chunk=parse_line))
    variables['humn'] = None

    def build_node(label):
        val = variables[label]
        if not isinstance(val, tuple):
            return Node(label, val)
        
        operator, a, b = val
        return Node(label, op=operator, left=build_node(a), right=build_node(b))
    
    root = build_node('root')
    root.op = eq
    root.simplify()

    # humn in left branch
    while (node := root.left).has_children():
        if node.left.is_known:
            known, unknown = node.get_children()
        else:
            unknown, known = node.get_children()
        
        if node.op is add:
            root.right = Node(node.name, op=sub, left=root.right, right=known)
        elif node.op is mul:
            root.right = Node(node.name, op=truediv, left=root.right, right=known)
        elif node.op is sub:
            op = add if known is node.right else sub
            root.right = Node(node.name, op=op, left=known, right=root.right)
        elif node.op is truediv:
            op = mul if known is node.right else truediv
            root.right = Node(node.name, op=op, left=known, right=root.right)

        root.left = unknown
        root.simplify()

    return root.right.value


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
