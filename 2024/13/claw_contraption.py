from utils import read_input, run, add
from functools import cache


FNAME = "13/input.txt"


def parse_input(input_file):

    def parse_chunk(chunk):
        lines = chunk.split('\n')
        return ((int(lines[i].split()[-2][2:].strip(',')), int(lines[i].split()[-1][2:])) for i in range(3))

    return read_input(input_file, parse_chunk=parse_chunk, separator='\n\n')


##########
# PART 1 #
##########


@cache
def fewest_tokens(button_a, button_b, prize, current=(0, 0), presses=0):
    if (presses > 200):
        return None
    if any(xy > prize_xy for xy, prize_xy in zip(current, prize)):
        return None

    if current == prize:
        return 0
    
    a_pressed = fewest_tokens(button_a, button_b, prize, add(current, button_a), presses+1)
    b_pressed = fewest_tokens(button_a, button_b, prize, add(current, button_b), presses+1)

    if a_pressed is None and b_pressed is None:
        return None
    
    if a_pressed is None:
        return 1 + b_pressed
    
    if b_pressed is None:
        return 3 + a_pressed
    
    return min(3 + a_pressed, 1 + b_pressed)



def part_one(input_file):
    machines = parse_input(input_file)
    return sum(token for token in (fewest_tokens(*machine) for machine in machines) if token is not None)


##########
# PART 2 #
##########


def tokens(button_a, button_b, prize):
    ax, ay = button_a
    bx, by = button_b
    px, py = prize

    px += 10000000000000
    py += 10000000000000

    b_presses = (ax * py - ay * px) / (ax * by - ay * bx)
    a_presses = (py - by * b_presses) / ay

    if int(a_presses) != a_presses or int(b_presses) != b_presses:
        return 0

    return int(3 * a_presses + b_presses)
    


def part_two(input_file):
    machines = list(parse_input(input_file))
    return sum(tokens(*machine) for machine in machines)
    


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
