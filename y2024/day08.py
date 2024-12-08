from utilities import timer
import itertools


def add_to_dict_list(dct, key, value):
    if key in dct:
        dct[key].append(value)
    else:
        dct[key] = [value]


@timer
def parse(file_name):
    table = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            table.append([x for x in line.strip()])

    antennas = dict()
    for y, row in enumerate(table):
        for x, letter in enumerate(row):
            if letter != ".":
                add_to_dict_list(antennas, letter, (x, y))
    return table, antennas


@timer
def part01(table, antennas):
    max_x = len(table[0]) - 1
    max_y = len(table) - 1

    antinodes = set()
    for ant in antennas.values():
        for p1, p2 in itertools.combinations(ant, 2):
            step =  p1[0] - p2[0], p1[1] - p2[1]
            if 0 <= p1[0] + step[0] <= max_x and 0 <= p1[1] + step[1] <= max_y:
                antinodes.add((p1[0] + step[0], p1[1] + step[1]))
            if 0 <= p2[0] - step[0] <= max_x and 0 <= p2[1] - step[1] <= max_y:
                antinodes.add((p2[0] - step[0], p2[1] - step[1]))
    return len(antinodes)


@timer
def part02(table, antennas):
    max_x = len(table[0]) - 1
    max_y = len(table) - 1

    antinodes = set()
    for k, ant in antennas.items():
        for p1, p2 in itertools.combinations(ant, 2):
            step_size = p1[0] - p2[0], p1[1] - p2[1]
            step = 0, 0
            while 0 <= p1[0] + step[0] <= max_x and 0 <= p1[1] + step[1] <= max_y:
                antinodes.add((p1[0] + step[0], p1[1] + step[1]))
                step = step[0] + step_size[0], step[1] + step_size[1]
            step = 0, 0
            while 0 <= p1[0] + step[0] <= max_x and 0 <= p1[1] + step[1] <= max_y:
                antinodes.add((p1[0] + step[0], p1[1] + step[1]))
                step = step[0] - step_size[0], step[1] - step_size[1]
    return len(antinodes)


if __name__ == "__main__":
    data = parse("day08.txt")
    print(part01(*data))
    print(part02(*data))
