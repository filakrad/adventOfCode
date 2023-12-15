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


def turn_90_clockwise(matrix):
    return [[matrix[i][j] for i in reversed(range(len(matrix)))] for j in range(len(matrix[0]))]


def tilt(matrix):
    y_max = len(matrix)
    for c in range(len(matrix[0])):
        square_indexes = []
        circle_nums = []
        now_circles = 0
        for r in range(y_max):
            if matrix[r][c] == '#':
                circle_nums.append(now_circles)
                square_indexes.append(r)
                now_circles = 0
            elif matrix[r][c] == 'O':
                now_circles += 1
        circle_nums.append(now_circles)
        first = circle_nums.pop(0)

        for i in range(y_max):
            matrix[i][c] = '.'
        for i in range(first):
            matrix[i][c] = 'O'

        for j, sq in enumerate(square_indexes):
            matrix[sq][c] = '#'
            for i in range(circle_nums[j]):
                matrix[sq + 1 + i][c] = 'O'
    return matrix


def do_cycle(matrix):
    for _ in range(4):
        matrix = tilt(matrix)
        matrix = turn_90_clockwise(matrix)
    return matrix


@timer
def part02(data):
    data = [[c for c in r] for r in data]

    memory = dict()
    cycle = 0
    while True:
        data = do_cycle(data)
        cycle += 1
        key = ''.join([''.join(r) for r in data])
        if key in memory:
            start_len = memory[key]
            cycle_len = cycle - memory[key]
            break
        memory[key] = cycle

    todo_cycles = (1000000000 - start_len) % cycle_len

    for _ in range(todo_cycles):
        data = do_cycle(data)

    total = 0
    y_max = len(data)
    for i, row in enumerate(data):
        for c in row:
            if c == 'O':
                total += y_max - i
    return total




if __name__ == "__main__":
    data = parse("data.txt")
    print(data)
    print(part01(data))
    print(part02(data))
