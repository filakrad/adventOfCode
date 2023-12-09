from y2023 import parser
from y2023.utilities import timer


@timer
def parse(file_name):
    return parser.load_rows_to_list(file_name=file_name, parse_function=lambda x: [int(i) for i in x.split(' ')])

@timer
def part01(data):
    total = 0
    for row in data:
        ends = [row[-1]]
        while not all(x == 0 for x in row):
            row = [i[1] - i[0] for i in zip(row, row[1:])]
            ends.append(row[-1])
        total += sum(ends)
    return total


@timer
def part02(data):
    total = 0
    for row in data:
        starts = [row[0]]
        while not all(x == 0 for x in row):
            row = [i[1] - i[0] for i in zip(row, row[1:])]
            starts.append(row[0])
        up = 0
        for s in reversed(starts):
            up = s - up
        total += up
    return total


if __name__ == "__main__":
    data = parse("data.txt")
    print(data)
    print(part01(data))
    print(part02(data))
