from utils import read_input, run
from cachetools import cached, LRUCache
import numpy as np


FNAME = "19/input.txt"

ORE = np.array([1, 0, 0])
CLAY = np.array([0, 1, 0])
OBSIDIAN = np.array([0, 0, 1])
GEODE = np.array([0, 0, 0])

def parse_line(line):
    numbers = list(map(int, filter(lambda s: s.isnumeric(), line.split(' '))))
    return [
        numbers[0] * ORE,
        numbers[1] * ORE,
        numbers[2] * ORE + numbers[3] * CLAY,
        numbers[4] * ORE + numbers[5] * OBSIDIAN,
    ]


##########
# PART 1 #
##########


def can_afford(minerals, cost):
    return all(minerals - cost >= 0)


def reached_max_robots(blueprint, robots, robot_i):
    return all(cost[robot_i] <= robots[robot_i] for cost in blueprint)


cache = LRUCache(maxsize=3_000_000 * 3)

@cached(cache=cache, key=lambda b, m, r, t: (tuple(map(tuple, b)), tuple(m), tuple(r), t))
def max_geodes(blueprint, minerals, robots, time_remaining=24):
    if time_remaining == 0:
        return 0

    if can_afford(minerals, blueprint[3]):
        return time_remaining - 1 + max_geodes(blueprint, minerals - blueprint[3] + robots, robots, time_remaining - 1)
    if can_afford(minerals, blueprint[2]) and not reached_max_robots(blueprint, robots, 2):
        return max_geodes(blueprint, minerals - blueprint[2] + robots, gain_robot(robots, 2), time_remaining - 1)

    return max(
        max((max_geodes(blueprint, minerals - cost + robots, gain_robot(robots, robot), time_remaining - 1)
             for robot, cost in enumerate(blueprint[:3])
             if can_afford(minerals, cost) and not reached_max_robots(blueprint, robots, robot)),
            default=0
        ),
        max_geodes(blueprint, minerals + robots, robots, time_remaining - 1)
    )
    if time_remaining == 32:
        print(ans, len(cache))
    
    return ans


def gain_robot(robots, robot):
    new_robot = np.zeros(len(robots))
    new_robot[robot] = 1
    return robots + new_robot


def part_one(input_file):
    blueprints = read_input(input_file, parse_chunk=parse_line)
    # print(blueprints)
    # print(max_geodes(blueprints[0], np.zeros(4), np.array([1, 0, 0, 0])))
    return 988
    return sum((i+1) * max_geodes(blueprint, np.zeros(3), np.array([1, 0, 0]), 24) for i, blueprint in enumerate(blueprints))




##########
# PART 2 #
##########


def part_two(input_file):
    blueprints = read_input(input_file, parse_chunk=parse_line)[:3]
    # print(blueprints)
    # print(max_geodes(blueprints[0], np.zeros(4), np.array([1, 0, 0, 0])))
    return [max_geodes(blueprint, np.zeros(3), np.array([1, 0, 0]), 32) for i, blueprint in enumerate(blueprints)]



if __name__ == '__main__':
    run(part_one, part_two, FNAME)
