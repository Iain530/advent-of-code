from utils import read_input, run
from operator import mul
from functools import reduce


FNAME = "02/input.txt"


##########
# PART 1 #
##########

def parse_chunk(line: str):
    game_number, all_hands = line.split(':')
    game_id = int(game_number.split()[1])
    hands = all_hands.split(';')

    return game_id, [{
        cubes.split()[1]: int(cubes.split()[0])
        for cubes in hand.strip().split(', ')
    } for hand in hands]



def is_possible(game, total_cubes):
    return all(
        count <= total_cubes.get(color, 0)
        for hand in game
        for color, count in hand.items()
    )



def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_chunk)
    total_cubes = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
    return sum(game_id for game_id, game in data if is_possible(game, total_cubes))


##########
# PART 2 #
##########




def power(game):
    return reduce(mul, (max(hand.get(color, 0) for hand in game) for color in ('red', 'green', 'blue')), 1)


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_chunk)
    return sum(power(game) for _, game in data)



if __name__ == '__main__':
    run(part_one, part_two, FNAME)
