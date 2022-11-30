from utils import read_input


if __name__ == "__main__":
    depths = read_input('day1/input.txt', types=[int])

    current, *depths = depths
    increases = 0

    for depth in depths:
        if depth > current:
            increases += 1
        current = depth

    print(increases)
