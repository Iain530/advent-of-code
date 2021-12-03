from utils import read_input


if __name__ == '__main__':
    input_commands = read_input('day2/input.txt', types=[str, int])

    aim = 0
    depth = 0
    horizontal = 0
    for direction, distance in input_commands:
        if direction == 'forward':
            horizontal += distance
            depth += aim * distance
        elif direction == 'down':
            aim += distance
        elif direction == 'up':
            aim -= distance

    print(f'D({depth}) * H({horizontal}) = {depth * horizontal}')
