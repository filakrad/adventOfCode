import re
import sys

from y2023.utilities import timer


@timer
def parse(file_name):
    total = dict()
    with open(file_name, "r") as f:
        all = f.read()
        parts = all.split("\n\n")
        seeds = parts.pop(0)
        total["seed"] = [int(x.group()) for x in re.finditer("[0-9]+", seeds)]
        total["rest"] = dict()
        for part in parts:
            lines = part.split("\n")
            legend = lines.pop(0)
            legend = legend.split(" ")[0].split("-")
            key = (legend[0], legend[-1])
            total["rest"][key] = []
            for row in lines:
                total["rest"][key].append([int(x.group()) for x in re.finditer("[0-9]+", row)])
    return total


@timer
def part01(data):
    minimum = sys.maxsize
    for seed in data["seed"]:
        from_, to_ = None, "seed"
        current = seed
        while to_ != "location":
            key = next(x for x in data["rest"].keys() if x[0] == to_)
            from_, to_ = key
            for row in data["rest"][key]:
                if row[1] <= current < row[1] + row[2]:
                    current = row[0] + current - row[1]
                    break
        minimum = min(minimum, current)
    return minimum


@timer
def part02(data):
    seed_length = len(data["seed"])
    seed_parts = list(zip([data["seed"][i] for i in range(0, seed_length, 2)], [data["seed"][i] for i in range(1, seed_length, 2)]))
    minimum = sys.maxsize
    min_seed = 0
    step = 1000
    for sp in seed_parts:
        for seed in range(sp[0], sp[0] + sp[1], step):
            from_, to_ = None, "seed"
            current = seed
            while to_ != "location":
                key = next(x for x in data["rest"].keys() if x[0] == to_)
                from_, to_ = key
                for row in data["rest"][key]:
                    if row[1] <= current < row[1] + row[2]:
                        current = row[0] + current - row[1]
                        break
            if current < minimum:
                minimum = current
                min_seed = seed
        print(f"part {sp} finished")

    minimum = sys.maxsize
    for seed in range(min_seed - step, min_seed + step):
        if not any(sp[0] <= seed < sp[0] + sp[1] for sp in seed_parts):
            continue
        from_, to_ = None, "seed"
        current = seed
        while to_ != "location":
            key = next(x for x in data["rest"].keys() if x[0] == to_)
            from_, to_ = key
            for row in data["rest"][key]:
                if row[1] <= current < row[1] + row[2]:
                    current = row[0] + current - row[1]
                    break
        if current < minimum:
            minimum = current
    return minimum


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))