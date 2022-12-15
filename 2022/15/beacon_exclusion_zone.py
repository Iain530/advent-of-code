from utils import read_input, run
from collections import Counter


FNAME = "15/input.txt"


def parse_line(line):
    return [tuple(int(coord.rstrip(',')[2:]) for coord in item.split(' ')[-2:]) for item in line.split(':')]


##########
# PART 1 #
##########

def distance(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    return abs(x2 - x1) + abs(y2 - y1)


def find_not_possible(data, target_y):
    not_possible = set()

    for sensor, beacon in data:
        x, y = sensor
        dist = distance(sensor, beacon)
        remaining_dist = dist - abs(target_y - y)
        if remaining_dist >= 0:
            not_possible |= {x + i for i in range(-remaining_dist, remaining_dist)}
    
    return not_possible


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    return len(find_not_possible(data, 2_000_000))

##########
# PART 2 #
##########


def is_correct(data, coord):
    return all(distance(sensor, coord) > distance(sensor, beacon) for sensor, beacon in data)


def find_outer_coords(counter: Counter, sensor, beacon):
    dist = distance(sensor, beacon) + 1
    x, y = sensor

    # Possible optimisation: just store the lines for each square
    # only consider points that intersect
    for i in range(dist):
        for edge_x in (x + dist - i, x - dist + i):
            for edge_y in (y-i, y+i):
                if 0 <= edge_x <= 4_000_000 and 0 <= edge_y <= 4_000_000:
                    counter[(edge_x, edge_y)] += 1

    return counter


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    counts = Counter()

    for sensor, beacon in data:
        find_outer_coords(counts, sensor, beacon)

    if answer := next((p for p in counts if counts[p] >= 4 and is_correct(data, p)), None):
        x, y = answer
        return x * 4_000_000 + y
    
    return None


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
