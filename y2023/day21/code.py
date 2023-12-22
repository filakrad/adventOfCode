from y2023.utilities import timer


@timer
def parse(file_name):
    data = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            data.append([x for x in line])
    return data


dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

@timer
def part01(data):
    starts = [[(x, y) for x, c in enumerate(r) if c == 'S'] for y, r in enumerate(data)]
    for s in starts:
        if s:
            start = s[0]

    max_y = len(data)
    max_x = len(data[0])

    current = [start]
    possible = set()
    for step in range(65):
        print(step)
        if step % 2 == 0:
            for x in current:
                possible.add(x)
        tmp = []
        for p in current:
            for d in dirs:
                next_p = p[0] + d[0], p[1] + d[1]
                x, y = next_p
                if 0 <= x < max_x and 0 <= y < max_y and next_p not in possible and data[y][x] != '#':
                    data[y][x] = '#'
                    tmp.append(next_p)
        current = tmp
    return len(possible)





@timer
def part02(data):
    pass


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))
