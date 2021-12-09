import math

from days import parser


def check_lowest(data, x, y):
    p = data[y][x]
    return p < min(data[y-1][x], data[y+1][x], data[y][x-1], data[y][x+1])


def part01(data):
    low_points = []
    for y in range(1, len(data)-1):
        for x in range(1, len(data[y])-1):
            if check_lowest(data, x, y):
                low_points.append((data[y][x], x, y))
    return low_points
    return sum([i[0] for i in low_points]) + len(low_points)


def get_higher_points(data, x, y, basin=set()):
    if (x, y) in basin:
        return
    else:
        basin.add((x, y))
    p = data[y][x]
    if p < data[y-1][x] < 9:
        get_higher_points(data, x, y-1, basin)
    if p < data[y+1][x] < 9:
        get_higher_points(data, x, y+1, basin)
    if p < data[y][x-1] < 9:
        get_higher_points(data, x-1, y, basin)
    if p < data[y][x+1] < 9:
        get_higher_points(data, x+1, y, basin)
    return basin


def part02(data, low_points):
    basin_lengths = []
    for p in low_points:
        basin = get_higher_points(data, p[1], p[2], set())
        basin_lengths.append(len(basin))
    basin_lengths.sort(reverse=True)
    return math.prod(basin_lengths[:3])

if __name__ == "__main__":
    data = parser.load_rows_to_list("day09.txt", lambda l: [10] + [int(x) for x in l.strip()] + [10])
    data = [[10 for _ in data[0]]] + data + [[10 for _ in data[0]]]
    low_points = part01(data)
    print(sum([i[0] for i in low_points]) + len(low_points))
    print(part02(data, low_points))