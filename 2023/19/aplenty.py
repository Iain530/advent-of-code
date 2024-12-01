from utils import read_input, run
from operator import gt, lt


FNAME = "19/input.txt"


def parse_chunk(para: str):
    if para.strip().startswith('{'):
        res = []
        for line in para.strip().split():
            res.append({rating[0]: int(rating[2:]) for rating in line.strip('{}').split(',')})
        return res
    
    res = {}
    for line in para.strip().split():
        name, rest = line.split('{')
        instructions = []
        for instruct in rest.rstrip('}').split(','):
            if ':' in instruct:
                cond, dest = instruct.split(':')
                instructions.append((cond[0], cond[1], int(cond[2:]), dest))
            else:
                instructions.append((instruct,))
        res[name] = instructions
    return res


##########
# PART 1 #
##########


OP_TO_FN = {
    '>': gt,
    '<': lt,
}
    


def execute_rule(gear, rule) -> str:
    for instruction in rule:
        print(len(instruction))
        if len(instruction) == 4:
            rating, op, value, dest = instruction
            if OP_TO_FN[op](gear[rating], value):
                return dest
        elif len(instruction) == 1:
            return instruction[0]
    raise Exception('No destination found')


def is_accepted(gear, rules) -> bool:
    out = 'in'
    while out not in ('R', 'A'):
        out = execute_rule(gear, rules[out])
    return out == 'A'


def part_one(input_file):
    rules, gears = read_input(input_file, separator='\n\n', parse_chunk=parse_chunk) 
    return sum(sum(gear.values()) for gear in gears if is_accepted(gear, rules))


##########
# PART 2 #
##########


def part_two(input_file):
    pass


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
