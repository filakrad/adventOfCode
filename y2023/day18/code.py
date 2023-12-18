from y2023.utilities import timer


dirs = {
    'U': (0, -1),
    'L': (-1, 0),
    'D': (0, 1),
    'R': (1, 0)
}


@timer
def parse(file_name):
    data = []
    with open(file_name, 'r') as f:
        for lin in f.readlines():
            parts = lin.strip().split(' ')
            color = parts[2].replace('(', '').replace(')', '').replace('#', '')
            data.append((parts[0], int(parts[1]), color))
    return data



@timer
def part01(data):
    # fin field size
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    curr = [0, 0]
    for d in data:
        if d[0] == 'D':
            curr[1] = curr[1] + d[1]
            max_y = max(max_y, curr[1])
        elif d[0] == 'U':
            curr[1] = curr[1] - d[1]
            min_y = min(min_y, curr[1])
        elif d[0] == 'R':
            curr[0] = curr[0] + d[1]
            max_x = max(max_x, curr[0])
        elif d[0] == 'L':
            curr[0] = curr[0] - d[1]
            min_x = min(min_x, curr[0])
    # print(min_x, min_y, max_x, max_y)
    field = [['.' for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]
    pos = [0 - min_x, 0 - min_y]
    field[pos[1]][pos[0]] = '#'

    #dig around
    for d in data:
        for _ in range(d[1]):
            pos[0] += dirs[d[0]][0]
            pos[1] += dirs[d[0]][1]
            field[pos[1]][pos[0]] = '#'

    #dig center
    stack = []
    for i, row in enumerate(field):
        if row[0] == '#' and row[1] == '.':
            stack.append((1, i))
            break
    print(stack)
    while stack:
        c = stack.pop()
        if not (0 <= c[0] < max_x - min_x and 0 <= c[1] < max_y - min_y ):
            continue
        if field[c[1]][c[0]] != '.':
            continue
        field[c[1]][c[0]] = '#'
        for d in dirs.values():
            stack.append((c[0] + d[0], c[1] + d[1]))

    for row in field:
        print(''.join(row))

    # count
    total = 0
    for row in field:
        total += sum([1 for c in row if c == '#'])

    return total






@timer
def part02(data):
    pass


if __name__ == "__main__":
    data = parse("data.txt")
    # print(data)
    print(part01(data))
    print(part02(data))
