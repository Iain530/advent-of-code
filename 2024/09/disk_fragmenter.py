from utils import read_input, run


FNAME = "09/input.txt"


def parse_input(input_file):
    data = read_input(input_file, parse_chunk=lambda l: list(map(int, l)))[0]
    disk = []
    for i, size in enumerate(data):
        if i % 2 == 0:
            disk += [i // 2] * size
        else:
            disk += [None] * size
    return disk


##########
# PART 1 #
##########


def next_free(disk, pointer: int = 0) -> int:
    while disk[pointer] is not None:
        pointer += 1
    return pointer


def next_block_reverse(disk, pointer) -> int:
    while disk[pointer] is None:
        pointer -= 1
    return pointer


def defrag(disk: list[int]) -> list[int]:
    free_i = next_free(disk)
    block_i = next_block_reverse(disk, len(disk) - 1)

    while free_i < block_i:
        disk[free_i] = disk[block_i]
        disk[block_i] = None
        free_i = next_free(disk, free_i)
        block_i = next_block_reverse(disk, block_i)


def checksum(disk):
    return sum(file_id * pos for pos, file_id in enumerate(disk) if file_id is not None)


def part_one(input_file):
    disk = parse_input(input_file)
    defrag(disk)
    return checksum(disk)


##########
# PART 2 #
##########


def free_space_size(disk, pointer):
    size = 0
    while disk[pointer] is None:
        size += 1
        pointer += 1
    return size


def find_free_space_start(disk, pointer):
    while disk[pointer] is not None:
        pointer += 1
    return pointer


def first_free_space(disk, size, stop):
    pointer = 0
    while pointer < stop:
        pointer = find_free_space_start(disk, pointer)
        found_size = free_space_size(disk, pointer)
        if found_size >= size and pointer < stop:
            return pointer
        else:
            pointer += found_size
    
    return None


def start_of_last_file(disk):
    pointer = len(disk) - 1
    size = 1
    file_id = disk[pointer]
    while disk[pointer - 1] == file_id:
        pointer -= 1
        size += 1
    return pointer, size



def next_file_reverse(disk, pointer):
    pointer -= 1
    while disk[pointer] is None:
        pointer -= 1
    file_id = disk[pointer]
    size = 1
    while disk[pointer - 1] == file_id:
        pointer -= 1
        size += 1
    return pointer, size


def move_file(disk, file_start, file_size, free_start):
    for i in range(file_size):
        if disk[free_start + i] is not None:
            raise Exception('Tried to overwrite file')
        disk[free_start + i] = disk[file_start + i]
        disk[file_start + i] = None


def defrag_files(disk):
    seen = set()
    file_start, file_size = start_of_last_file(disk)

    while file_start > 0:
        if disk[file_start] not in seen:
            free_space = first_free_space(disk, file_size, file_start)
            seen.add(disk[file_start])
            if free_space:
                move_file(disk, file_start, file_size, free_space)
        file_start, file_size = next_file_reverse(disk, file_start)


def part_two(input_file):
    disk = parse_input(input_file)
    defrag_files(disk)
    return checksum(disk)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
