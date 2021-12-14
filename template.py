from utils import read_input, timed

fname = "dayX/input.txt"


##########
# PART 1 #
##########


def part_one():
    data = read_input(fname)
    print(data)


##########
# PART 2 #
##########


def part_two():
    pass


if __name__ == '__main__':
    print("PART 1")
    result, time = timed(part_one)
    print(f"Answer:\t{result}\nTime:\t{time*1000}ms")
    print()
    print(f"PART 2")
    result, time = timed(part_two)
    print(f"Answer:\t{result}\nTime:\t{time*1000}ms")
