from utils import read_input, run
from typing import List, Generator, Tuple
from dataclasses import dataclass
from functools import cache

fname = "day21/input.txt"


def parse(fname):
    lines = list(read_input(fname, types=[str, str, str, str, int]))
    return lines[0][-1], lines[1][-1]


##########
# PART 1 #
##########


@dataclass
class Dice:
    value: int = 0
    rolled_count: int = 0

    def roll_deterministic(self) -> int:
        self.value += 1
        self.rolled_count += 1
        return self.value


def make_rolls(dice: Dice, n: int = 3) -> List[int]:
    return [dice.roll_deterministic() for _ in range(n)]


def move_spaces(current: int, move: int) -> int:
    return (current - 1 + move) % 10 + 1 


def take_turn(dice, score, position):
    rolls = make_rolls(dice)
    position = move_spaces(position, sum(rolls))
    score += position
    return score, position


def play(start_positions: Tuple[int, int]):
    dice = Dice()
    p1_position, p2_position = start_positions
    p1_score = p2_score = 0
    while True:
        p1_score, p1_position = take_turn(dice, p1_score, p1_position)
        if p1_score >= 1000:
            return p2_score * dice.rolled_count
        p2_score, p2_position = take_turn(dice, p2_score, p2_position)
        if p2_position >= 1000:
            return p1_score * dice.rolled_count


def part_one():
    positions = parse(fname)
    return play(positions)


##########
# PART 2 #
##########


def take_quantum_turn(position, score, roll_sum):
    position = move_spaces(position, roll_sum)
    score += position
    return position, score


quantum_dice_roll_sums = [
    sum((i, j, k)) for i in range(1, 4) for j in range(1, 4) for k in range(1, 4)
]


@cache
def play_quantum(positions: Tuple[int, int], scores: Tuple[int, int], is_p1_turn: bool) -> Tuple[int, int]:
    p1_score, p2_score = scores
    if p1_score >= 21:
        return 1, 0
    elif p2_score >= 21:
        return 0, 1
    
    p1_pos, p2_pos = positions
    total_p1_wins = total_p2_wins = 0
    for roll_sum in quantum_dice_roll_sums:
        if is_p1_turn:
            new_position, new_score = take_quantum_turn(p1_pos, p1_score, roll_sum)
            p1_wins, p2_wins = play_quantum((new_position, p2_pos), (new_score, p2_score), False)
        else:
            new_position, new_score = take_quantum_turn(p2_pos, p2_score, roll_sum)
            p1_wins, p2_wins = play_quantum((p1_pos, new_position), (p1_score, new_score), True)
        total_p1_wins += p1_wins
        total_p2_wins += p2_wins

    return total_p1_wins, total_p2_wins
    

def part_two():
    positions = parse(fname)
    return max(play_quantum(positions, (0, 0), True))


if __name__ == '__main__':
    run(part_one, part_two)
