from y2023.utilities import timer, replace_str_index


@timer
def parse(file_name):
    data = []
    with open(file_name, "r") as f:
        whole = f.read()
    parts = whole.split("\n\n")
    for p in parts:
        data.append(p.split("\n"))
    return data


def test(p, last = -1):
    total = 0
    max_y = len(p)
    max_x = len(p[0])
    # test horizontal
    for center in range(1, max_y):
        steps = min(center, max_y - center)
        if all(p[center-1-step][i] == p[center+step][i] for step in range(steps) for i in range(max_x)):
            total = 100*center
            if total != last:
                return total

    # test vertical
    for center in range(1, max_x):
        steps = min(center, max_x - center)
        if all(p[i][center-1-step] == p[i][center+step] for step in range(steps) for i in range(max_y)):
            total = center
            if total != last:
                return total
    return total


@timer
def part01(data):
    total = 0
    for p in data:
        total += test(p)
    return total


@timer
def part02(data):
    other = {'.': '#', '#': '.'}
    total = 0
    for p in data:
        max_y = len(p)
        max_x = len(p[0])
        old = test(p)
        for c in range(max_y * max_x):
            y = c // max_x
            x = c % max_x
            p[y] = replace_str_index(p[y], x, other[p[y][x]])
            tot = test(p, old)
            if tot and tot != old:
                total += tot
                break
            p[y] = replace_str_index(p[y], x, other[p[y][x]])
    return total


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))
