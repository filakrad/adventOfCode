from utilities import timer


@timer
def parse(file_name):
    data = []
    with open(file_name, "r") as f:
        for line in f:
            nums = [int(x) for x in line.strip().split(" ")]
            data.append(nums)
    return data


def is_safe(levels):
    difs = [x[0] - x[1] for x in zip(levels, levels[1:])]
    sgn = difs[0]
    if all([sgn * x > 0 and 1 <= abs(x) <= 3 for x in difs]):
        return True
    return False


@timer
def part01(data):
    return sum([is_safe(levels) for levels in data])


@timer
def part02(data):
    total = 0
    for idx, levels in enumerate(data):
        if any([is_safe(levels[:i] + levels[i + 1:]) for i in range(len(levels))]):
            total += 1
    return total


if __name__ == "__main__":
    data = parse("day02.txt")
    print(part01(data))
    print(part02(data))
