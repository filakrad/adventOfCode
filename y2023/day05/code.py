import re

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
    locations = []
    for d, v in data["rest"].items():
        v.sort(key=lambda x: x[0])
    for seed in data["seed"]:
        from_, to_ = None, "seed"
        current = seed
        while to_ != "location":
            key = next(x for x in data["rest"].keys() if x[0] == to_)
            from_, to_ = key
            next_ = None
            for row in data["rest"][key]:
                if current in range(row[1], row[1] + row[2]):
                    next_ = row[0] + current - row[1]
                    break

            if next_ is None:
                out_idx = current - sum(x[2] for x in data["rest"][key] if x[1] < current)
                now = 0
                for row in data["rest"][key]:
                    if row[0] < now + out_idx:
                        out_idx -= row[0] - now
                        now += row[2]
                    else:
                        break
                next_ = now + out_idx
            # print(from_, to_, current, next_)

            current = next_
        locations.append(next_)
    return min(locations)


@timer
def part02(data):
    pass


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))