import re
import collections

from y2023.utilities import timer


@timer
def parse(file_name):
    Race = collections.namedtuple('Race', ['time', 'distance'])
    with open(file_name, "r") as f:
        time = f.readline()
        distance = f.readline()
        time = [int(x.group()) for x in re.finditer("[0-9]+", time)]
        distance = [int(x.group()) for x in re.finditer("[0-9]+", distance)]
    return map(Race, time, distance)


@timer
def parse02(file_name):
    Race = collections.namedtuple('Race', ['time', 'distance'])
    with open(file_name, "r") as f:
        time = "".join(f.readline().split())
        distance = "".join(f.readline().split())
        time = [int(x.group()) for x in re.finditer("[0-9]+", time)]
        distance = [int(x.group()) for x in re.finditer("[0-9]+", distance)]
    return map(Race, time, distance)


@timer
def part01(data):
    total = 1
    for t in data:
        winning = [i*(t.time-i) for i in range(t.time) if i*(t.time-i) > t.distance]
        total *= len(winning)
    return total


@timer
def part02(data):
    pass


if __name__ == "__main__":
    file_name = "data.txt"
    data = parse(file_name)
    print(part01(data))
    data = parse02(file_name)
    print(part01(data))