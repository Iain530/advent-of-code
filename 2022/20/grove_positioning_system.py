from utils import read_input, run, run_test


FNAME = "20/input.txt"


##########
# PART 1 #
##########


def move(lst: list, start_i: int, end_i: int):
    item = lst.pop(start_i)
    lst.insert(end_i, item)


def find_start_end_indexes(data, mixed, i):
    start_i = mixed.index((i, data[i]))
    end_i = (start_i + data[i]) % (len(data) - 1)
    if end_i == 0:
        end_i = len(data) - 1
    return start_i, end_i


def part_one(input_file):
    data = read_input(input_file, parse_chunk=lambda l: int(l))
    count = len(data)
    mixed = list(enumerate(data))

    for i in range(count):
        start_i, end_i = find_start_end_indexes(data, mixed, i)
        move(mixed, start_i, end_i)

    result = [d[1] for d in mixed]
    zero_i = result.index(0)
    return sum(result[(zero_i + interval) % count] for interval in (1000, 2000, 3000))


##########
# PART 2 #
##########


def part_two(input_file):
    data = [d * 811589153 for d in read_input(input_file, parse_chunk=lambda l: int(l))]    
    count = len(data)
    mixed = list(enumerate(data))

    for _ in range(10):
        for i in range(count):
            start_i, end_i = find_start_end_indexes(data, mixed, i)
            move(mixed, start_i, end_i)

    result = [d[1] for d in mixed]
    zero_i = result.index(0)
    return sum(result[(zero_i + interval) % count] for interval in (1000, 2000, 3000))


if __name__ == '__main__':
    run_test(part_one, '20/test_input.txt', 3, 'Part 1 Example input')
    run_test(part_two, '20/test_input.txt', 1623178306, 'Part 2 Example input')
    run(part_one, part_two, FNAME)
