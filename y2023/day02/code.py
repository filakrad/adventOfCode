import re

from y2023.utilities import timer

def match_color(text):
    red = re.search("[0-9]+ red", text)
    r = int(red.group().split(" ")[0]) if red is not None else 0
    green = re.search("[0-9]+ green", text)
    g = int(green.group().split(" ")[0]) if green is not None else 0
    blue = re.search("[0-9]+ blue", text)
    b = int(blue.group().split(" ")[0]) if blue is not None else 0
    return (r, g, b)


@timer
def parse(file_name):
    print(file_name)
    with open(file_name, "r") as f:
        games = dict()
        line = f.readline()
        while line:
            game, rest = line.split(":")
            game_id = int(game.split(" ")[1])
            subsets = []
            subsets_str = rest.split(";")
            for s in subsets_str:
                subsets.append(match_color(s))
            games[game_id] = subsets
            line = f.readline()
    return games


@timer
def part01(data):
    sum = 0
    for k, v in data.items():
        is_bad = any([x[0] > 12 or x[1] > 13 or x[2] > 14 for x in v])
        if not is_bad:
            sum += k
    return sum


@timer
def part02(data):
    sum = 0
    for k, v in data.items():
        power = max(x[0] for x in v) * max(x[1] for x in v) * max(x[2] for x in v)
        sum += power
    return sum


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))