from math import ceil, floor

def read_input(fname):
    with open(fname) as f:
        return [int(n) for n in f.read().strip().split(',')]


fname = "day7/input.txt"


##########
# PART 1 #
##########


def part_one():
    positions = read_input(fname)

    min_pos = min(positions)
    max_pos = max(positions)

    min_cost = min(sum(abs(pos - target) for pos in positions) for target in range(min_pos, max_pos))

    return min_cost


##########
# PART 2 #
##########


def cost(distance):
    return (distance * (distance + 1)) // 2


def part_two():
    positions = read_input(fname)

    min_pos = min(positions)
    max_pos = max(positions)

    min_cost = min(sum(cost(abs(pos - target)) for pos in positions) for target in range(min_pos, max_pos))

    return min_cost


if __name__ == '__main__':
    print("Part 1")
    print(part_one())
    print("Part 2")
    print(part_two())
