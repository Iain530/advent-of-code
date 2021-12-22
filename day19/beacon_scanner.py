from collections import defaultdict
from typing import Tuple, overload
import numpy as np
from utils import run
from itertools import permutations

fname = "day19/input.txt"


def read_input(fname):
    data = []
    with open(fname) as f:
        scanners = f.read().split('\n\n')
        for scanner in scanners:
            data.append(np.array([
                list(map(int, line.split(',')))
                for line in scanner.split('\n')[1:]
            ]))
    return data

##########
# PART 1 #
##########


def pair_offsets(scanner):
    offsets = set()
    for b1, b2 in permutations(scanner, 2):
        v = b2 - b1
        offsets.add(tuple(v))
    return offsets


def rotated(scanner, r=1):
    return np.roll(scanner, r, axis=1)


def create_all_offsets(scanners):
    offsets = defaultdict(dict)
    for i, scanner in enumerate(scanners):
        for rot in range(len(scanner[0])):
            offsets[i][rot] = pair_offsets(rotated(scanner, rot))
    return offsets


def is_overlapping(offsets, s1: Tuple[int, int], s2: Tuple[int, int], overlap_amount=3) -> bool:
    s1_no, s1_rot = s1
    s2_no, s2_rot = s2
    return len(offsets[s1_no][s1_rot] & offsets[s2_no][s2_rot]) >= overlap_amount


def find_next_overlapping(offsets, overlaps):
    for scanner_no, rotations in offsets.items():
        if scanner_no in overlaps:
            continue
        for known_scanner, (_, known_scanner_rot) in overlaps.items():
            for rot in rotations.keys():
                if is_overlapping(offsets, (scanner_no, rot), (known_scanner, known_scanner_rot)):
                    overlaps[scanner_no] = (known_scanner, rot)
                    return


def find_overlapping(offsets):
    overlaps = {
        0: (0, 0)
    } # (scanner_no, rot) where rot is relative to scanner 0
    while len(overlaps) < len(offsets):
        find_next_overlapping(offsets, overlaps)

    return overlaps


def part_one():
    scanners = read_input(fname)
    offsets = create_all_offsets(scanners)
    # print(scanners[0])
    # print(rotated(scanners[0]))
    # print(pair_offsets(scanners[0]), pair_offsets(rotated(scanners[0])))
    # print(offsets)
    print(find_overlapping(offsets))


##########
# PART 2 #
##########


def part_two():
    pass


if __name__ == '__main__':
    run(part_one, part_two)
