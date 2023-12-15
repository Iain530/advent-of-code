from utils import read_input, run
from functools import reduce
from collections import defaultdict, OrderedDict


FNAME = "15/input.txt"


def parse_line(line: str) -> list[str]:
    return line.split(',')


##########
# PART 1 #
##########


def hash_character(current: int, character: str) -> int:
    return ((current + ord(character)) * 17) % 256


def hash_string(string: str) -> int:
    return reduce(hash_character, string, 0)


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)[0]
    return sum(hash_string(s) for s in data)
    

##########
# PART 2 #
##########


def process_step(step: str, boxes: dict[int, dict[str, int]]) -> None:
    op = step[2]
    if step[-1] == '-':
        label = step[:-1]
        if label in (box := boxes[hash_string(label)]):
            del box[label]
    elif step[-2] == '=':
        label = step[:-2]
        boxes[hash_string(label)][label] = int(step[-1])
    else:
        raise Exception(f'Invalid operation {op}, {step}')


def focal_power(boxes: dict):
    return sum(
        sum(
            (box_no + 1) * (i + 1) * focal_length
            for i, focal_length in enumerate(box.values())
        )
        for box_no, box in boxes.items()
    )


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_line)[0]
    boxes = defaultdict(OrderedDict)
    for step in data:
        process_step(step, boxes)
    return focal_power(boxes)





if __name__ == '__main__':
    run(part_one, part_two, FNAME)
