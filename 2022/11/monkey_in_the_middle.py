from utils import read_input, run
from dataclasses import dataclass
from collections import deque, defaultdict
from operator import add, mul
from typing import Callable
from functools import cache


FNAME = "11/input.txt"
LCM = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19


@dataclass
class Monkey:
    id: int
    items: deque[int]
    operation: Callable[[int], int]
    next_monkey: Callable[[int], int]
    inspections: int = 0

    def has_items(self):
        return bool(self.items)
    
    def next_item(self):
        return self.items.popleft()
    
    def inspect(self, item, is_part_one=True):
        self.inspections += 1
        worry = self.operation(item)

        if is_part_one:
            worry //= 3
        else:
            worry %= LCM
        
        return worry, self.next_monkey(worry)

    def recieve_item(self, item):
        self.items.append(item)


OPERATORS = {
    '+': add,
    '*': mul
}


def parse_chunk(chunk):
    lines = chunk.splitlines()
    number = int(lines[0].split()[-1][:-1])
    items = deque(map(int, lines[1][18:].split(', ')))
    
    op_symbol, last = lines[2].split()[-2:]
    op = OPERATORS[op_symbol]

    if last == 'old':
        variable = lambda old: old
    else:
        variable = lambda _: int(last)

    def operation(old):
        return op(old, variable(old))

    test_divisible = int(lines[3].split()[-1])
    true_monkey = int(lines[4].split()[-1])
    false_monkey = int(lines[5].split()[-1])

    def next_monkey(worry_level):
        if worry_level % test_divisible == 0:
            return true_monkey
        return false_monkey

    return Monkey(number, items, operation, next_monkey)


##########
# PART 1 #
##########


def round(monkeys, is_part_one=True):
    for monkey in monkeys:
        while monkey.has_items():
            item = monkey.next_item()
            item, next_monkey = monkey.inspect(item, is_part_one)
            monkeys[next_monkey].recieve_item(item)


def part_one(input_file):
    monkeys = read_input(input_file, separator='\n\n', parse_chunk=parse_chunk)
    
    for _ in range(20):
        round(monkeys)

    return mul(*sorted(m.inspections for m in monkeys)[-2:])


##########
# PART 2 #
##########


def part_two(input_file):
    monkeys = read_input(input_file, separator='\n\n', parse_chunk=parse_chunk)
    
    for _ in range(10000):
        round(monkeys, is_part_one=False)

    return mul(*sorted(m.inspections for m in monkeys)[-2:])


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
