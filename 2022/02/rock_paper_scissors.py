from utils import read_input, run


FNAME = "02/input.txt"


def parse_line(line):
    return tuple(line.strip().split())


##########
# PART 1 #
##########

WIN = 6
DRAW = 3
LOSE = 0

def part_one(input_file):
    base_scores = {
        'X': 1,
        'Y': 2,
        'Z': 3,
    }
    outcomes = {
        'A': {
            'X': DRAW,
            'Y': WIN,
            'Z': LOSE,
        },
        'B': {
            'X': LOSE,
            'Y': DRAW,
            'Z': WIN,
        },
        'C': {
            'X': WIN,
            'Y': LOSE,
            'Z': DRAW,
        },
    }
    data = read_input(input_file, parse_chunk=parse_line)
    return sum(base_scores[me] + outcomes[elf][me] for elf, me in data)


##########
# PART 2 #
##########

CHOICES = ['A', 'B', 'C']
SHIFT = {
    'X': -1,
    'Y': 0,
    'Z': 1,
}
OUTCOME_SCORES = {
    'X': LOSE,
    'Y': DRAW,
    'Z': WIN,
}
BASE_SCORES = {
    'A': 1,
    'B': 2,
    'C': 3,
}


def choose_response(elf, strategy):
    elf_i = CHOICES.index(elf)
    return CHOICES[(elf_i + SHIFT[strategy]) % 3]


def score_game(game):
    elf, strategy = game
    me = choose_response(elf, strategy)
    return BASE_SCORES[me] + OUTCOME_SCORES[strategy]


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    return sum(score_game(game) for game in data)
    


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
