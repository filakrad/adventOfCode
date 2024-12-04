from utilities import timer
import itertools


@timer
def parse(file_name):
    data = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            data.append(line.strip())
    return data


@timer
def part01(data):
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    text = "XMAS"
    total = 0
    xmax = len(data[0]) - 1
    ymax = len(data) - 1
    tries = itertools.product(range(len(data[0])), range(len(data)), dirs)
    for t in tries:
        for step, letter in enumerate(text):
            y = t[1] + step * t[2][1]
            x = t[0] + step * t[2][0]
            if x < 0 or x > xmax or y < 0 or y > ymax:
                break
            if data[y][x] != letter:
                break
        else:
            total += 1
    return total


@timer
def part02(data):
    dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    total = 0
    xmax = len(data[0]) - 1
    ymax = len(data) - 1
    tries = itertools.product(range(len(data[0])), range(len(data)))
    for t in tries:
        if data[t[1]][t[0]] != 'A':
            continue
        cnt = 0
        for d in dirs:
            y1 = t[1] + d[1]
            x1 = t[0] + d[0]
            y2 = t[1] + d[1] * -1
            x2 = t[0] + d[0] * -1
            if x1 < 0 or x1 > xmax or y1 < 0 or y1 > ymax:
                break
            if x2 < 0 or x2 > xmax or y2 < 0 or y2 > ymax:
                break
            if data[y1][x1] == 'M' and data[y2][x2] == 'S':
                cnt += 1
        if cnt == 2:
            total += 1
    return total


if __name__ == "__main__":
    data = parse("day04.txt")
    print(part01(data))
    print(part02(data))
