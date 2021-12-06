from collections import defaultdict


fname = "day6/input.txt"


def read_input(fname):
    with open(fname) as f:
        ages = list(map(int, f.read().strip().split(',')))
    fish = defaultdict(int)
    for age in ages:
        fish[age] += 1
    return fish


##########
# PART 1 #
##########


def simulate(fish):
    next_state = defaultdict(int)
    for i in range(1, 9):
        next_state[i-1] = fish[i]
    next_state[6] += fish[0]
    next_state[8] += fish[0]
    return next_state


def solve(fish, days):
    for _ in range(days):
        fish = simulate(fish)
    return fish


def part_one():
    fish = read_input(fname)
    fish = solve(fish, days=80)
    return sum(fish.values())


##########
# PART 2 #
##########


def part_two():
    fish = read_input(fname)
    fish = solve(fish, days=256)
    return sum(fish.values())


if __name__ == '__main__':
    print("Part 1")
    print(part_one())
    print("Part 2")
    print(part_two())
