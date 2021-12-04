from dataclasses import dataclass
from typing import List, Dict, Tuple
from pprint import pp

fname = 'day4/input.txt'

@dataclass
class Cell:
    number: int
    marked: bool = False


@dataclass(init=False)
class Board:
    rows: List[List[Cell]]
    number_positions: Dict[int, Tuple[int, int]]

    @property
    def columns(self):
        return list(zip(*self.rows))

    def __init__(self, rows) -> None:
        self.rows = rows
        self.number_positions = dict()
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                self.number_positions[cell.number] = (i, j)

    def mark(self, number: int) -> None:
        pos = self.number_positions.get(number)
        if pos:
            i, j = pos
            self.rows[i][j].marked = True

    def is_complete(self) -> bool:
        return (
            any(all(cell.marked for cell in row) for row in self.rows) or
            any(all(cell.marked for cell in col) for col in self.columns)
        )
    
    def sum_unmarked(self):
        return sum(cell.number for row in self.rows for cell in row if cell.marked is False)

    def __contains__(self, number: int):
        return number in self.number_positions


def read_input():
    with open(fname) as f:
        raw_numbers, *raw_boards = f.read().strip().split('\n\n')
    numbers = list(map(int, raw_numbers.split(',')))
    boards = [
        Board([
            [
                Cell(int(n)) for n in row.split()
            ]
            for row in raw_board.split('\n')
        ])
        for raw_board in raw_boards
    ]
    return numbers, boards


##########
# PART 1 #
##########


def part_one():
    numbers, boards = read_input()

    for number in numbers:
        for board in boards:
            if number in board:
                board.mark(number)
                if board.is_complete():
                    pp([[c.number for c in r] for r in board.rows])
                    return board.sum_unmarked(), number



##########
# PART 2 #
##########


def part_two():
    numbers, boards = read_input()
    boards_left = len(boards)

    for number in numbers:
        for board in boards:
            if number in board and not board.is_complete():
                board.mark(number)
                if board.is_complete():
                    if boards_left > 1:
                        boards_left -= 1
                    else:
                        pp([[c.number for c in r] for r in board.rows])
                        return board.sum_unmarked(), number


if __name__ == '__main__':
    print("Part 1")
    board_sum, number = part_one()
    print(f"{board_sum=} * {number=} = {board_sum * number}")

    print("Part 2")
    board_sum, number = part_two()
    print(f"{board_sum=} * {number=} = {board_sum * number}")
