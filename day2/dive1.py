from utils import read_input


if __name__ == '__main__':

    input_commands = read_input('day2/input.txt', types=[str, int])

    depth = 0
    horizontal = 0
    for direction, distance in input_commands:
        if direction == 'forward':
            horizontal += distance
        elif direction == 'down':
            depth += distance
        elif direction == 'up':
            depth -= distance

    print(f'D({depth}) * H({horizontal}) = {depth * horizontal}')
