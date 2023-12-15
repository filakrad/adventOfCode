from y2023.utilities import timer


@timer
def parse(file_name):
    with open(file_name, "r") as f:
        data = f.readline().split(',')
    return data


def HASH(step):
    curr = 0
    for char in step:
        curr += ord(char)
        curr *= 17
        curr %= 256
    return curr


@timer
def part01(data):
    total = 0
    for step in data:
        total += HASH(step)
    return total


@timer
def part02(data):
    boxes = {i: [] for i in range(256)}
    for step in data:
        if '-' in step:
            label, lng = step.split('-')
        else:
            label, lng = step.split("=")
        box = HASH(label)
        if lng == '':
            for i, lens in enumerate(boxes[box]):
                if lens[0] == label:
                    boxes[box].pop(i)
                    break
        else:
            for i, lens in enumerate(boxes[box]):
                if lens[0] == label:
                    boxes[box][i] = [label, lng]
                    break
            else:
                boxes[box].append([label, lng])

    total = 0
    for i in range(256):
        for j, b in enumerate(boxes[i]):
            total += (i+1) * (j+1) * int(b[1])
    return total


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))
