


fname = 'day5/input.txt'


def read_input():
    with open(fname) as f:
        lines = [
            l.strip().split(' -> ')
            for l in f.readlines()
        ]
        return [
            [
                tuple(map(int, coord.split(',')))
                for coord in line
            ]
            for line in lines
        ]


##########
# PART 1 #
##########


def solve(ignore_diagonal=True):
    lines = read_input()
    grid = [[0] * 1000 for _ in range(1000)]

    for (x1, y1), (x2, y2) in lines:
        x_dir = x2 - x1
        if x_dir != 0:
            x_dir //= abs(x_dir)
        
        y_dir = y2 - y1
        if y_dir != 0:
            y_dir //= abs(y_dir)
        
        if ignore_diagonal:
            if x_dir != 0 and y_dir != 0:
                continue

        while (x1, y1) != (x2, y2):
            grid[y1][x1] += 1
            x1 += x_dir
            y1 += y_dir
        grid[y1][x1] += 1
        x1 += x_dir
        y1 += y_dir

    return sum(1 for row in grid for cell in row if cell > 1)


def part_one():
    return solve()


##########
# PART 2 #
##########


def part_two():
    return solve(ignore_diagonal=False)


if __name__ == '__main__':
    print(f"Part 1 = {part_one()}")
    print(f"Part 2 = {part_two()}")
