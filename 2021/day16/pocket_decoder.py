import operator
from typing import Callable, Generator, List, Tuple
from utils import run
from collections import deque
from functools import reduce

ProcessPacketResultType = Tuple[List[int], int, int]

fname = "day16/input.txt"


def read_input(fname: str) -> str:
    with open(fname) as f:
        return f.read().strip()


##########
# PART 1 #
##########


def read(stream: deque, n: int = 1, as_int: bool = True):
    binary = ''.join(stream.popleft() for _ in range(n))
    if as_int:
        return bin_to_dec(binary)
    return binary


def hex_to_bin(hex: str) -> int:
    return (bin(int(hex, 16))[2:]).zfill(len(hex) * 4)


def bin_to_dec(binary: str) -> int:
    return int(binary, 2)


def read_header(stream: deque) -> Tuple[int, int]:
    version = read(stream, 3)
    packet_type = read(stream, 3)
    return version, packet_type
    

def process_literal_value(stream: deque) -> int:
    more = True
    values = []
    while more:
        more = bool(read(stream, 1))
        value = read(stream, 4, as_int=False)
        values.append(value)
    return bin_to_dec(''.join(values))


def process_subpackets(stream: deque) -> Generator[ProcessPacketResultType, None, None]:
    I = read(stream)
    if I == 0:
        consumed = 0
        subpacket_bits = read(stream, 15)
        while consumed < subpacket_bits:
            versions, packet_length, value = process_packet(stream)
            yield versions, packet_length, value
            consumed += packet_length
    else:
        subpackets = read(stream, 11)
        yield from (process_packet(stream) for _ in range(subpackets))


def process_operator(stream: deque, op: Callable[..., int]) -> Tuple[List[int], int]:
    versions = []
    values = []
    for sub_versions, _, value in process_subpackets(stream):
        versions += sub_versions
        values.append(value)
    return versions, op(*values)


def process_packet(stream: deque) -> ProcessPacketResultType:
    packet_start = len(stream)
    version, packet_type = read_header(stream)
    versions = [version]
    if packet_type == 4:
        value = process_literal_value(stream)
    else:
        subpacket_versions, value = process_operator(stream, OPERATORS[packet_type])
        versions += subpacket_versions
    packet_length = packet_start - len(stream)
    return versions, packet_length, value


def part_one():
    data = read_input(fname)
    binary = hex_to_bin(data)
    stream = deque(binary)
    versions, _, _ = process_packet(stream)
    return sum(versions)


##########
# PART 2 #
##########


OPERATORS = {
    0: lambda *nums: sum(nums),
    1: lambda *nums: reduce(operator.mul, nums),
    2: lambda *nums: min(nums),
    3: lambda *nums: max(nums),
    5: operator.gt,
    6: operator.lt,
    7: operator.eq,
}


def part_two():
    data = read_input(fname)
    binary = hex_to_bin(data)
    stream = deque(binary)
    _, _, value = process_packet(stream)
    return value


if __name__ == '__main__':
    run(part_one, part_two)
