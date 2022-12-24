from utils import read_input, run, run_test
from operator import mul
from collections import defaultdict


FNAME = "23/input.txt"


def add(c1, c2):
    return tuple(a + b for a, b in zip(c1, c2))


E = (0, 1)
S = (1, 0)
W = (0, -1)
N = (-1, 0)
SE = add(S, E)
SW = add(S, W)
NW = add(N, W)
NE = add(N, E)


def parse_input(input_file):
    data = read_input(input_file, parse_chunk=lambda l: l)
    elves = set()

    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if char == '#':
                elves.add((i, j))
    return elves


##########
# PART 1 #
##########


def are_adjacent_free(elves, pos, directions):
    return not elves.intersection({add(pos, d) for d in directions})


def starting_directions():
    return [
        (N, NE, NW),
        (S, SE, SW),
        (W, NW, SW),
        (E, NE, SE),
    ]


DIRECTIONS = starting_directions()


def propose_move(elves, pos):
    if not are_adjacent_free(elves, pos, [N, E, S, W, NE, SE, SW, NW]):
        for directions in DIRECTIONS:
            if are_adjacent_free(elves, pos, directions):
                # print("moving")
                return add(pos, directions[0])
    return pos


def smallest_rectangle(elves):
    def key(i):
        return lambda e: e[i]

    height = max(elves, key=key(0))[0] - min(elves, key=key(0))[0] + 1
    width = max(elves, key=key(1))[1] - min(elves, key=key(1))[1] + 1
    
    return width * height


def simulate_round(elves):
    proposed_positions = defaultdict(set) 
    for e in elves:
        proposed_positions[propose_move(elves, e)].add(e)
    
    new_elves = set()
    for new_pos, old_positions in proposed_positions.items():
        if len(old_positions) == 1:
            new_elves.add(new_pos)
        else:
            new_elves |= old_positions
    
    DIRECTIONS.append(DIRECTIONS.pop(0))
    return new_elves


def part_one(input_file):
    elves = parse_input(input_file)
    
    for _ in range(10):
        elves = simulate_round(elves)
        
    return smallest_rectangle(elves) - len(elves)


##########
# PART 2 #
##########


def part_two(input_file):
    global DIRECTIONS
    DIRECTIONS = starting_directions()
    elves = parse_input(input_file)
    
    round_no = 1
    while True:
        new_elves = simulate_round(elves)
        if new_elves == elves:
            break
        elves = new_elves
        round_no += 1
        
    return round_no


if __name__ == '__main__':
    # run_test(part_one, '23/test_input.txt', 25, 'Example input')
    run(part_one, part_two, FNAME)
