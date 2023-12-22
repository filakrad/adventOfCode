import copy

from y2023.utilities import timer


@timer
def parse(file_name):
    bricks = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            a, b = line.split('~')
            a = tuple(int(x) for x in a.split(','))
            b = tuple(int(x) for x in b.split(','))
            if a[2] < b[2]:
                bricks.append((a, b))
            elif b[2] < a[2]:
                bricks.append((b, a))
            elif a[1] < b[1]:
                bricks.append((a, b))
            elif b[1] < a[1]:
                bricks.append((b, a))
            elif a[0] < b[0]:
                bricks.append((a, b))
            elif b[0] < a[0]:
                bricks.append((b, a))
            else:
                bricks.append((b, a))
    bricks.sort(key=lambda x: x[0][2])
    return bricks


def brick_fall(data):
    min_x = min(min(x[0][0], x[1][0]) for x in data)
    max_x = max(max(x[0][0], x[1][0]) for x in data)
    min_y = min(min(x[0][1], x[1][1]) for x in data)
    max_y = max(max(x[0][1], x[1][1]) for x in data)
    field_height = [[0 for _ in range(min_x, max_x+1)] for _ in range(min_y, max_y+1)]
    field_label = [[-1 for _ in range(min_x, max_x+1)] for _ in range(min_y, max_y+1)]
    supports = {i: set() for i in range(-1, len(data))}
    supported_by = {i: set() for i in range(-1, len(data))}
    for i, brick in enumerate(data):
        brick_height = brick[1][2] - brick[0][2] + 1
        brick_coords = []
        for p in range(brick[0][0], brick[1][0] + 1):
            for q in range(brick[0][1], brick[1][1] + 1):
                brick_coords.append((p, q))
        top = max(field_height[q][p] for p, q in brick_coords)
        for p, q in brick_coords:
            if field_height[q][p] == top:
                supports[field_label[q][p]].add(i)
                supported_by[i].add(field_label[q][p])
            field_height[q][p] = top + brick_height
            field_label[q][p] = i
    return supports, supported_by


@timer
def part01(data):
    supports, supported_by = brick_fall(data)
    removable = 0
    for i in range(len(data)):
        if all(len(supported_by[k]) > 1 for k in supports[i]):
            removable += 1
    return removable




@timer
def part02(data):
    # Finished 'part02' in 16.5388413 secs
    # Would be better with reversed brick order and memoization
    supports, supported_by = brick_fall(data)

    del supported_by[-1]
    total = 0
    for i in range(len(data)):
        tmp_supported_by = copy.deepcopy(supported_by)
        to_delete = [i]
        while to_delete:
            for d in to_delete:
                del tmp_supported_by[d]
                for by in tmp_supported_by.values():
                    by.discard(d)
            to_delete = []
            for k, by in tmp_supported_by.items():
                if len(by) == 0:
                    total += 1
                    to_delete.append(k)

    return total


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))
