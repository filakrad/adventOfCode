from itertools import combinations

from y2023.parser import load_rows_to_list
from y2023.utilities import timer



@timer
def parse(file_name):
    data = load_rows_to_list(file_name)
    data = [[x for x in row.strip()] for row in data]
    return data


def expand_universe(data):
    cols = [c for c in range(len(data[0])) if all(row[c] == '.' for row in data)]
    for c in reversed(cols):
        for row in data:
            row.insert(c, '.')

    rows = [i for i, r in enumerate(data) if len(set(r)) == 1 and set(r).pop() == '.']
    for r in reversed(rows):
        data.insert(r, ['.' for _ in data[0]])

    return data


@timer
def part01(data):
    data = expand_universe(data)
    galaxies = [(x, y) for y, row in enumerate(data) for x, s in enumerate(row) if s == '#']
    pairs = combinations(galaxies, 2)
    return sum(abs(x[1][0] - x[0][0]) + abs(x[1][1] - x[0][1]) for x in pairs)


@timer
def part02(data):
    cols = [c for c in range(len(data[0])) if all(row[c] == '.' for row in data)]
    rows = [i for i, r in enumerate(data) if len(set(r)) == 1 and set(r).pop() == '.']

    galaxies = [(x, y) for y, row in enumerate(data) for x, s in enumerate(row) if s == '#']
    pairs = combinations(galaxies, 2)

    total = 0
    expansion_rate = 1000000
    for p, q in pairs:
        xs = sorted([p[0], q[0]])
        x = xs[1] - xs[0] + len([c for c in cols if xs[0] < c < xs[1]]) * (expansion_rate - 1)
        ys = sorted([p[1], q[1]])
        y = ys[1] - ys[0] + len([r for r in rows if ys[0] < r < ys[1]]) * (expansion_rate - 1)
        total += x + y
    return total


if __name__ == "__main__":
    file_name = 'data.txt'
    data = parse(file_name)
    print(part01(data))
    data = parse(file_name)
    print(part02(data))
