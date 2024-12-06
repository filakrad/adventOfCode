import copy

from utilities import timer


@timer
def parse(file_name):
    data = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            data.append([x for x in line.strip()])
    return data


@timer
def part01(data_input):
    data = copy.deepcopy(data_input)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    max_y = len(data) - 1
    max_x = len(data[0]) - 1
    start_y = [i for i, row in enumerate(data) if '^' in row][0]
    start_x = data[start_y].index("^")
    curr_pos = (start_x, start_y)
    dir_index = 0
    while True:
        data[curr_pos[1]][curr_pos[0]] = "X"
        next_pos = (curr_pos[0] + directions[dir_index % 4][0], curr_pos[1] + directions[dir_index % 4][1])
        if next_pos[0] < 0 or next_pos[0] > max_x or next_pos[1] < 0 or next_pos[1] > max_y:
            break
        while data[next_pos[1]][next_pos[0]] == "#":
            dir_index += 1
            next_pos = (curr_pos[0] + directions[dir_index % 4][0], curr_pos[1] + directions[dir_index % 4][1])
        curr_pos = next_pos
    return sum([x.count("X") for x in data])


def check_for_loop(data_input):
    data = copy.deepcopy(data_input)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    max_y = len(data) - 1
    max_x = len(data[0]) - 1
    start_y = [i for i, row in enumerate(data) if '^' in row][0]
    start_x = data[start_y].index("^")
    curr_pos = (start_x, start_y)
    dir_index = 0
    visited = set()
    loop = False
    while True:
        step = (curr_pos[0], curr_pos[1], dir_index % 4)
        if step in visited:
            loop = True
            break
        visited.add(step)
        next_pos = (curr_pos[0] + directions[dir_index % 4][0], curr_pos[1] + directions[dir_index % 4][1])
        if next_pos[0] < 0 or next_pos[0] > max_x or next_pos[1] < 0 or next_pos[1] > max_y:
            break
        while data[next_pos[1]][next_pos[0]] == "#":
            dir_index += 1
            next_pos = (curr_pos[0] + directions[dir_index % 4][0], curr_pos[1] + directions[dir_index % 4][1])
        curr_pos = next_pos
    return loop

@timer
def part02(data_input):

    data = copy.deepcopy(data_input)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    max_y = len(data) - 1
    max_x = len(data[0]) - 1
    start_y = [i for i, row in enumerate(data) if '^' in row][0]
    start_x = data[start_y].index("^")
    curr_pos = (start_x, start_y)
    dir_index = 0
    path = set()
    while True:
        path.add(curr_pos)
        next_pos = (curr_pos[0] + directions[dir_index % 4][0], curr_pos[1] + directions[dir_index % 4][1])
        if next_pos[0] < 0 or next_pos[0] > max_x or next_pos[1] < 0 or next_pos[1] > max_y:
            break
        while data[next_pos[1]][next_pos[0]] == "#":
            dir_index += 1
            next_pos = (curr_pos[0] + directions[dir_index % 4][0], curr_pos[1] + directions[dir_index % 4][1])
        curr_pos = next_pos

    loops = 0
    for pos in path:
        tmp = data[pos[1]][pos[0]]
        data[pos[1]][pos[0]] = "#"
        if pos != (start_x, start_y):
            if check_for_loop(data):
                loops += 1
        data[pos[1]][pos[0]] = tmp

    return loops


if __name__ == "__main__":
    data = parse("day06.txt")
    print(part01(data))
    print(part02(data))
