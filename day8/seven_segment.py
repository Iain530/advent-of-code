from collections import Counter, defaultdict


fname = "day8/input.txt"


def parse(fname):
    with open(fname) as f:
        lines = (line.strip() for line in f.readlines())

    data = []
    for line in lines:
        patterns, output = line.strip().split('|')
        patterns = [frozenset(d) for d in patterns.strip().split()]
        output = [frozenset(d) for d in output.strip().split()]
        data.append((patterns, output))
    
    return data


##########
# PART 1 #
##########

SEGMENTS_PER_DIGIT = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}


def part_one():
    data = parse(fname)

    segment_counts = Counter()

    for _, output in data:
        for digit in output:
            segment_counts[len(digit)] += 1
    
    print(segment_counts)

    return sum(segment_counts[SEGMENTS_PER_DIGIT[n]] for n in (1, 4, 7, 8))


##########
# PART 2 #
##########


#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....

#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg


def zero_six_nine(six_segments, one, four):
    assert len(six_segments) == 3

    nine = next(pattern for pattern in six_segments if four < pattern)

    copy = set(six_segments)
    copy.remove(nine)

    a, b = copy
    if one < a:
        return a, b, nine
    return b, a, nine


def two_three_five(five_segments, one, six):
    assert len(five_segments) == 3

    three = next(pattern for pattern in five_segments if one < pattern)
    
    copy = set(five_segments)
    copy.remove(three)

    a, b = copy
    if len(six - a) == 1:
        return b, three, a
    
    return a, three, b


def solve(patterns, output):
    patterns_by_segment_count = defaultdict(list)
    for p in patterns:
        patterns_by_segment_count[len(p)].append(p)

    one = patterns_by_segment_count[SEGMENTS_PER_DIGIT[1]].pop()
    four = patterns_by_segment_count[SEGMENTS_PER_DIGIT[4]].pop()
    seven = patterns_by_segment_count[SEGMENTS_PER_DIGIT[7]].pop()
    eight = patterns_by_segment_count[SEGMENTS_PER_DIGIT[8]].pop()

    zero, six, nine = zero_six_nine(patterns_by_segment_count[6], one, four)
    two, three, five = two_three_five(patterns_by_segment_count[5], one, six)

    decoder = {
        zero: '0',
        one: '1',
        two: '2',
        three: '3',
        four: '4',
        five: '5',
        six: '6',
        seven: '7',
        eight: '8',
        nine: '9',
    }

    return int(''.join(decoder[o] for o in output))


def part_two():
    data = parse(fname)
    return sum(solve(patterns, output) for patterns, output in data)


if __name__ == '__main__':
    print("Part 1")
    print(part_one())
    print("Part 2")
    print(part_two())
