from utils import read_input, run


FNAME = "07/input.txt"


##########
# PART 1 #
##########


def split_beams(beams: set[int], row: str):
    next_beam = set()
    split = 0
    for beam in beams:
        if row[beam] == '^':
            split += 1
            next_beam |= {beam - 1, beam + 1}
        else:
            next_beam.add(beam)
    
    return next_beam, split


def part_one(input_file):
    start, *rows = read_input(input_file, parse_chunk=str)

    beams = {start.index('S')}
    count = 0
    for row in rows:
        beams, split = split_beams(beams, row)
        count += split
    
    return count


##########
# PART 2 #
##########


def split_quantum_beams(beams: list[int], row):
    for i, beam in enumerate(beams):
        if row[i] == '^':
            pass
            beams[i-1] += beam
            beams[i+1] += beam
            beams[i] = 0



def part_two(input_file):
    start, *rows = read_input(input_file, parse_chunk=str)

    beams = [0] * len(start)
    beams[start.index('S')] = 1

    for row in rows:
        split_quantum_beams(beams, row)
    
    return sum(beams)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
