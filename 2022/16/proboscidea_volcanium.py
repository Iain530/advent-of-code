from utils import read_input, run
from functools import cache


FNAME = "16/input.txt"


def parse_line(line):
    valve = line[6:8]
    flow_rate = int(line.split(' ')[4].rstrip(';')[5:])
    neighbours = [n[-2:] for n in line.split(', ')]
    return valve, flow_rate, neighbours


##########
# PART 1 #
##########


def release_pressure(data, open_valves):
    return sum(data[v][0] for v in open_valves)


def part_one(input_file):
    data = {valve: (flow, neighbours) for valve, flow, neighbours in read_input(input_file, parse_chunk=parse_line)}

    @cache
    def max_pressure(current, open_valves, time_remaining):
        flow, neighbours = data[current]
        
        if time_remaining == 0:
            return 0
        
        pressure = 0
        if flow > 0 and current not in open_valves:
            pressure = flow * (time_remaining - 1) + max_pressure(current, frozenset(open_valves | {current}), time_remaining - 1)
        
        return max(pressure, max(max_pressure(n, open_valves, time_remaining - 1) for n in neighbours))

    
    return max_pressure('AA', frozenset(), 30)


##########
# PART 2 #
##########



def part_two(input_file):
    data = {valve: (flow, neighbours) for valve, flow, neighbours in read_input(input_file, parse_chunk=parse_line)}

    @cache
    def max_elephant_pressure(current, open_valves, time_remaining):
        flow, neighbours = data[current]
        
        if time_remaining == 0:
            return 0
        
        if time_remaining == 26 and current != 'AA':
            return max_elephant_pressure('AA', open_valves, time_remaining)
        
        pressure = 0
        if flow > 0 and current not in open_valves:
            pressure = flow * (time_remaining % 26 - 1) + max_elephant_pressure(current, frozenset(open_valves | {current}), time_remaining - 1)
        
        return max(pressure, max(max_elephant_pressure(n, open_valves, time_remaining - 1) for n in neighbours))

    return max_elephant_pressure('AA', frozenset(), 26 * 2)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
