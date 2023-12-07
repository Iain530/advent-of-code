from utils import read_input, run
from collections import Counter
from enum import Enum


FNAME = "07/input.txt"
Hand = list[str]


def parse_line(line: str) -> tuple[Hand, int]:
    hand, bid = line.split()
    return list(hand), int(bid) 


##########
# PART 1 #
##########


class HandType(Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


CARD_ORDER = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}


def get_hand_type(hand: Hand) -> HandType:
    card_counts = sorted(Counter(hand).values())
    match card_counts:
        case [5]:
            return HandType.FIVE_OF_A_KIND
        case [1, 4]:
            return HandType.FOUR_OF_A_KIND
        case [2, 3]:
            return HandType.FULL_HOUSE
        case [1, 1, 3]:
            return HandType.THREE_OF_A_KIND
        case [1, 2, 2]:
            return HandType.TWO_PAIR
        case [1, 1, 1, 2]:
            return HandType.ONE_PAIR
        case [1, 1, 1, 1, 1]:
            return HandType.HIGH_CARD
        case _:
            raise Exception(f'{card_counts} not a valid hand')


def secondary_keys(hand: Hand) -> int:
    return (CARD_ORDER[c] for c in hand)


def key(hand: Hand) -> tuple:
    return (get_hand_type(hand).value, *(CARD_ORDER[c] for c in hand))


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    sorted_data = sorted(data, key=lambda d: key(d[0]))
    return sum((i + 1) * bid for i, (_, bid) in enumerate(sorted_data))


##########
# PART 2 #
##########


def use_joker(hand: Hand) -> Hand:
    counts = Counter(hand)
    if counts['J'] == 5:
        return hand
    most_common_non_joker = next(c[0] for c in counts.most_common(2) if c[0] != 'J')
    return list(''.join(hand).replace('J', most_common_non_joker, counts['J']))


def key_with_jokers(hand: Hand) -> tuple:
    return (get_hand_type(use_joker(hand)).value, *(CARD_ORDER[c] for c in hand))


def part_two(input_file):
    CARD_ORDER['J'] = 0
    data = read_input(input_file, parse_chunk=parse_line)
    sorted_data = sorted(data, key=lambda d: key_with_jokers(d[0]))
    return sum((i + 1) * bid for i, (_, bid) in enumerate(sorted_data))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
