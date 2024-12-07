from utils import read_input, run


FNAME = "05/input.txt"


def parse_input(input_file):
    rules_raw, updates_raw = read_input(input_file, separator='\n\n')
    rules = [tuple(r.split('|')) for r in rules_raw]
    updates = [l.split(',') for l in updates_raw]
    return rules, updates


##########
# PART 1 #
##########


def prepare(manual):
    return {page: i for i, page in enumerate(manual)}


def is_valid(indexed_manual, rules):
    for a, b in rules:
        if a in indexed_manual and b in indexed_manual:
            a_pos = indexed_manual[a]
            b_pos = indexed_manual[b]
            if b_pos < a_pos:
                return False
    return True


def middle(manual):
    return int(manual[len(manual) // 2])


def part_one(input_file):
    rules, updates = parse_input(input_file)
    return sum(middle(manual) for manual in updates if is_valid(prepare(manual), rules))


##########
# PART 2 #
##########


def recreate_manual(indexed_manual):
    return [k for k, v in sorted(indexed_manual.items(), key=lambda x: x[1])]


def make_valid(manual, rules):
    indexed = prepare(manual)
    while not is_valid(indexed, rules):
        for a, b in rules:
            if a in indexed and b in indexed:
                a_pos = indexed[a]
                b_pos = indexed[b]
                if b_pos < a_pos:
                    indexed[a] = b_pos
                    indexed[b] = a_pos
                    continue
    return recreate_manual(indexed)



def part_two(input_file):
    rules, updates = parse_input(input_file)
    return sum(middle(make_valid(manual, rules)) for manual in updates if not is_valid(prepare(manual), rules)) 


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
