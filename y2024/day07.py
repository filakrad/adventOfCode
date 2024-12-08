from utilities import timer
from itertools import product


@timer
def parse(file_name):
    dct = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            k, v = line.strip().split(":")
            dct.append([int(k), [int(x) for x in v.strip().split(" ")]])
    return dct


def add(x, y):
    return x + y


def mul(x, y):
    return x * y


@timer
def part01(data):
    total = 0
    for k, v in data:
        for ops in product([add, mul], repeat=len(v)-1):
            sub_result = v[0]
            for op, val in zip(ops, v[1:]):
                sub_result = op(sub_result, val)
            if sub_result == k:
                total += sub_result
                break
    return total


def concat(x, y):
    return int(f"{x}{y}")


@timer
def part02(data):
    total = 0
    for k, v in data:
        for ops in product([add, mul, concat], repeat=len(v)-1):
            sub_result = v[0]
            for op, val in zip(ops, v[1:]):
                sub_result = op(sub_result, val)
            if sub_result == k:
                total += sub_result
                break
    return total


if __name__ == "__main__":
    data = parse("day07.txt")
    print(part01(data))
    print(part02(data))
