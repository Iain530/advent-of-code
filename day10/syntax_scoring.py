from utils import read_input, run
from queue import LifoQueue

fname = "day10/input.txt"


##########
# PART 1 #
##########


BRACKET_PAIRS = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>',
}


UNEXPECTED_BRACKET_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


def first_unexpected_symbol(line):
    stack = LifoQueue()
    for symbol in line:
        if symbol in BRACKET_PAIRS:
            stack.put(BRACKET_PAIRS[symbol])
        else:
            expected = stack.get()
            if symbol != expected:
                return symbol 
    return None
    

def symbol_points(symbol):
    return UNEXPECTED_BRACKET_POINTS.get(symbol, 0)


def part_one():
    data = list(read_input(fname, types=[str]))
    
    return sum(symbol_points(first_unexpected_symbol(line)) for line in data)


##########
# PART 2 #
##########


AUTOCOMPLETE_BRACKET_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def autocomplete(line: str):
    stack = LifoQueue()
    for symbol in line:
        if symbol in BRACKET_PAIRS:
            stack.put(BRACKET_PAIRS[symbol])
        else:
            expected = stack.get()
            if symbol != expected:
                return None 
    return stack


def autocomplete_points(stack: LifoQueue):
    score = 0
    while not stack.empty():
        score *= 5
        symbol = stack.get()
        score += AUTOCOMPLETE_BRACKET_POINTS[symbol]
    
    return score


def part_two():
    data = read_input(fname, types=[str])
    completions = filter(bool, (autocomplete(line) for line in data))

    scores = sorted(autocomplete_points(c) for c in completions)
    median = scores[len(scores) // 2]

    return median


if __name__ == '__main__':
    run(part_one, part_two)
