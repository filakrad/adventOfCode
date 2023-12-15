from y2023.utilities import timer


@timer
def parse(file_name):
    data = []
    with open(file_name, "r") as f:
        for l in f.readlines():
            data.append(l.strip())
    return data


@timer
def part01(data):
    y_max = len(data)
    total = 0
    for c in range(len(data[0])):
        square_indexes = []
        circle_nums = []
        now_circles = 0
        for r in range(y_max):
            if data[r][c] == '#':
                circle_nums.append(now_circles)
                square_indexes.append(r)
                now_circles = 0
            elif data[r][c] == 'O':
                now_circles += 1
        circle_nums.append(now_circles)
        first = circle_nums.pop(0)
        total += sum(y_max - i for i in range(first))
        for j, sq in enumerate(square_indexes):
            total += sum((y_max - sq) - i - 1 for i in range(circle_nums[j]))
    return total


@timer
def part02(data):
    pass


if __name__ == "__main__":
    data = parse("data.txt")
    print(data)
    print(part01(data))
    print(part02(data))
