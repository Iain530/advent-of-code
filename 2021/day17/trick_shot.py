from utils import run

fname = "day17/input.txt"


def read_input(fname):
    with open(fname) as f:
        raw = f.read().strip()[13:]
        xy_data = raw.split(', ')
        return tuple(
            tuple(map(int, data[2:].split('..'))) for data in xy_data
        )


##########
# PART 1 #
##########


def sum_1_to_n(n):
    return n*(n+1) / 2


def find_converging_x(x_target):
    min_x, max_x = x_target
    return {i for i in range(max_x) if min_x <= sum_1_to_n(i) <= max_x}


def step(position, vx, vy):
    x, y = position
    return (x + vx, y + vy), max(vx - 1, 0), vy - 1



def is_possible(position, vx, vy, x_target, y_target):
    x, y = position
    min_x, max_x = x_target
    min_y, max_y = y_target
    return x <= max_x and (y >= min_y or vy >= 0) and (vx > 0 or x >= min_x)



def in_target(position, x_target, y_target):
    x, y = position
    min_x, max_x = x_target
    min_y, max_y = y_target
    return min_x <= x <= max_x and min_y <= y <= max_y


def simulate(vx, vy, x_target, y_target):
    initial_vx = vx
    initial_vy = vy
    position = (0, 0)
    max_y = position[1]
    while is_possible(position, vx, vy, x_target, y_target):
        position, vx, vy = step(position, vx, vy)
        if position[1] >= max_y:
            max_y = position[1]
        
        if in_target(position, x_target, y_target):
            return max_y, (initial_vx, initial_vy, position), True

    
    return 0, (initial_vx, initial_vy), False


def part_one():
    x_target, y_target = read_input(fname)
    converging_x = find_converging_x(x_target)

    results = (simulate(vx, vy, x_target, y_target) for vx in converging_x for vy in range(abs(min(y_target)) + 1))
    max_y = max(results, key=lambda r: r[0])[0]
    return max_y


##########
# PART 2 #
##########


def part_two():
    x_target, y_target = read_input(fname)
    converging_x = find_converging_x(x_target)
    min_x = min(converging_x)

    success_count = 0
    for vx in range(min_x, max(x_target) + 1):
        for vy in range(min(y_target), abs(min(y_target)) + 1):
            _, _, success = simulate(vx, vy, x_target, y_target)
            if success:
                success_count += 1
    return success_count


if __name__ == '__main__':
    run(part_one, part_two)
