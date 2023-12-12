from functools import lru_cache
import itertools
import re

from y2023.utilities import timer


@timer
def parse(file_name):
    data = []
    with open(file_name, "r") as f:
        for l in f.readlines():
            a, b = l.split(' ')
            b = [int(x) for x in b.split(',')]
            data.append((a, b))
    return data


def is_valid(test, expected):
    stripped = ".".join([x for x in test.split(".") if x])
    return all(len(x) == expected[i] for i, x in enumerate(stripped.split('.')))


@timer
def part01(data):
    total = 0
    subtots = []
    for h, row in enumerate(data):
        known_broken = row[0].count('#')
        needed_broken = sum(row[1]) - known_broken

        combs = itertools.combinations([m.start() for m in re.finditer('\?', row[0])], needed_broken)
        subtotal = 0
        for c in combs:
            test = "".join([x if x != '?' else '#' if i in c else '.' for i, x in enumerate(row[0])])
            if is_valid(test, row[1]):
                subtotal += 1

        subtots.append(subtotal)
        total += subtotal
    # print(subtots)
    return total


@lru_cache(maxsize=None)
def sliding_pattern(pattern, matches):
    if not pattern:
        return 0
    if len(pattern) < sum(matches) + len(matches) - 1:
        return 0

    total = 0
    matching = matches[0]
    max_i = min(pattern.index("#") + matching, len(pattern)) if "#" in pattern else len(pattern)
    parts = [pattern[i:i+matching] for i in range(max_i - matching + 1)]
    for i, part in enumerate(parts):
        if any(s == '.' for s in part): # no dots inside
            continue
        if i != 0: # no octothorpe before
            if pattern[i-1] == '#':
                continue
        if i + matching < len(pattern): # no octothorpe right after
            if pattern[i+matching] == '#':
                continue
        if len(matches) == 1:
            if "#" not in pattern[i+matching:]: # cant be any more octothorpes the after last
                total += 1
        else:
            t = sliding_pattern(pattern[i+matching+1:], matches[1:])
            total += t

    return total


@timer
def sliding_test(data):
    total = 0
    subtots=[]
    for i, row in enumerate(data):
        # if i != 5:
        #     continue
        subtotal = sliding_pattern(row[0], tuple(row[1]))
        sliding_pattern.cache_clear()
        total += subtotal
        subtots.append(subtotal)
    print(subtots)
    return total

@timer
def part02(data):
    total = 0
    for h, row in enumerate(data):
        new_row_0 = "?".join(itertools.repeat(row[0], 5))
        new_row_1 = list(itertools.chain.from_iterable(itertools.repeat(row[1], 5)))
        subtotal = sliding_pattern(new_row_0, tuple(new_row_1))
        sliding_pattern.cache_clear()
        total += subtotal
    return total


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(sliding_test(data)) # part 01 with part 02 technique
    print(part02(data))
