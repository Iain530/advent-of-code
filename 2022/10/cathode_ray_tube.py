from utils import read_input, run, sliding_window


FNAME = "10/input.txt"


def parse_line(line):
    split = line.split()
    if len(split) > 1:
        split[1] = int(split[1])
    return split


##########
# PART 1 #
##########


def simulate(data):
    values = []
    x = 1

    for op in data:
        match op:
            case ['addx', v]:
                values += [x, x]
                x += v
            case ['noop']:
                values += [x]
    
    return values


def signal_strength(values, cycle):
    return values[cycle - 1] * cycle


def part_one(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    register_values = simulate(data)
    return sum(signal_strength(register_values, cycle) for cycle in (20, 60, 100, 140, 180, 220))


##########
# PART 2 #
##########


def draw_row(row):
    return ''.join('#' if abs(cycle - value) <= 1 else '.' for cycle, value in enumerate(row))


def part_two(input_file):
    data = read_input(input_file, parse_chunk=parse_line)
    values = simulate(data)
    return '\n' + '\n'.join(draw_row(values[i:i+40]) for i in range(0, len(values), 40))


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
