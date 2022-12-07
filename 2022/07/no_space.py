from utils import read_input, run


FNAME = "07/input.txt"


def parse_ls(current_directory, data):
    while data and data[0][0] != '$':
        file_info = data.pop(0)
        match file_info:
            case ['dir', dir_name]:
                if dir_name not in current_directory:
                    current_directory[dir_name] = {}
            case [size, file_name]:
                current_directory[file_name] = int(size)


def load_directories(data):
    path = []
    root = dict()

    def current_dir():
        current = root
        for d in path:
            current = current[d]
        return current

    while data:
        command = data.pop(0)
        match command:
            case ['$', 'cd', '..']:
                path.pop()
            case ['$', 'cd', '/']:
                path = []
            case ['$', 'cd', dir_name]:
                path.append(dir_name)
            case ['$', 'ls']:
                parse_ls(current_dir(), data)

    return root

##########
# PART 1 #
##########


def find_all_subdirectories(directory):
    subdirs = []
    for entry in directory.values():
        if isinstance(entry, dict):
            subdirs += [entry] + find_all_subdirectories(entry)
    return subdirs


def dir_size(directory):
    total = 0
    for entry in directory.values():
        if isinstance(entry, int):
            total += entry 
        elif isinstance(entry, dict):
            total += dir_size(entry)
    return total


def part_one(input_file):
    data = read_input(input_file, parse_chunk=lambda l: l.split())
    root = load_directories(data)    

    all_directories = find_all_subdirectories(root)
    return sum(size for direcotry in all_directories if (size := dir_size(direcotry)) <= 100_000)


##########
# PART 2 #
##########


def part_two(input_file):
    data = read_input(input_file, parse_chunk=lambda l: l.split())
    root = load_directories(data)

    all_directories = find_all_subdirectories(root)
    needed = 30_000_000 - (70_000_000 - dir_size(root))

    return min(s for direcotry in all_directories if (s := dir_size(direcotry)) >= needed)


if __name__ == '__main__':
    run(part_one, part_two, FNAME)
