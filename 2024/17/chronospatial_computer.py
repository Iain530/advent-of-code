from utils import read_input, run


FNAME = "17/input.txt"


def parse_input(input_file):
    raw_registers, raw_program = read_input(input_file, separator='\n\n', parse_chunk=str)
    registers = tuple(int(l.split()[-1]) for l in raw_registers.splitlines())
    program = list(map(int, raw_program.split()[-1].split(',')))
    return registers, program



##########
# PART 1 #
##########


def simulate(a, b, c, program):
    instruction = 0
    jumped = False
    output = []

    def get_combo(operand: int) -> int:
        if operand in (0, 1, 2, 3):
            return operand
        
        if operand == 4:
            return a
        
        if operand == 5: 
            return b
        
        if operand == 6:
            return c
        
        raise Exception(f'Invalid operand: {operand}')
    
    def adv(operand):
        nonlocal a
        a = a // (2 ** get_combo(operand))
    
    def bxl(operand):
        nonlocal b
        b = b ^ operand

    def bst(operand):
        nonlocal b
        b = get_combo(operand) % 8
    
    def jnz(operand):
        nonlocal instruction, jumped
        if a == 0:
            return
        instruction = operand
        jumped = True
    
    def bxc(operand):
        nonlocal b
        b = b ^ c
    
    def out(operand):
        output.append(get_combo(operand) % 8)
    
    def bdv(operand):
        nonlocal b
        b = a // (2 ** get_combo(operand))
    
    def cdv(operand):
        nonlocal c
        c = a // (2 ** get_combo(operand))
        
    ops = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    def run():
        nonlocal instruction, jumped
        while instruction < len(program) - 1:
            ops[program[instruction]](program[instruction + 1])
            if not jumped:
                instruction += 2
            jumped = False

    run()
    return output



def part_one(input_file):
    (a, b, c), program = parse_input(input_file)
    output = simulate(a, b, c, program)
    return ','.join(map(str, output))

##########
# PART 2 #
##########

# a=7329105394703 (7)


def diff(output, program):
    return sum(1 for a, b in zip(output, program) if a != b) + abs(len(output) - len(program))


def part_two(input_file):
    (a, b, c), program = parse_input(input_file)
    a = 7329105394703
    output = []
    closest = []

    since_best = 0

    while output != program:
        output = simulate(a, b, c, program)
        if diff(output, program) < diff(closest, program) or not closest:
            print(f'New best: {diff(output, program)}, {a=}, {output=}, {program=}')
            closest = output
            a *= 10
            since_best = 0
        else:
            since_best += 1


        a += 1
        if diff(output, program) == diff(closest, program) or not closest:
            print(f'{a=}, {output=}, {program=}')
        

        if since_best > 1000000:
            a += 1000000
            since_best = 0
            print(f'skipping to {a}')

    return a


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
