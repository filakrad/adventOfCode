from y2023.utilities import timer

import sys
sys.setrecursionlimit(5000)


directions = "NESW"

coord = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}

from_to = {
    '.': {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'},
    '/': {'N': 'W', 'E': 'S', 'S': 'E', 'W': 'N'},
    '\\': {'N': 'E', 'E': 'N', 'S': 'W', 'W': 'S'},
    '-': {'N': 'EW', 'E': 'W', 'S': 'EW', 'W': 'E'},
    '|': {'N': 'S', 'E': 'NS', 'S': 'N', 'W': 'NS'}
}

opposite = {'N': 'S', 'W': 'E', 'S': 'N', 'E': 'W'}


@timer
def parse(file_name):
    board = []
    with open(file_name, "r") as f:
        lines = f.readlines()
        for l in lines:
            board.append(l.strip())
    return board


visited = set()


def energize(board, energ, x, y, dir):
    if (x, y, dir) in visited:
        return
    if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board):
        return
    else:
        visited.add((x, y, dir))
    energ[y][x] = 1
    for to_dir in from_to[board[y][x]][dir]:
        next_dir = opposite[to_dir]
        energize(board, energ, x + coord[next_dir][0], y + coord[next_dir][1], next_dir)


@timer
def part01(data):
    dir = 'E'
    energ = [[0 for _ in data[0]] for _ in data]
    energize(data, energ, 0, 0, dir)
    return sum(sum(r) for r in energ)


@timer
def part02(data): # crashes on stack overflow -- wtf???
    dirs =   [(0, i, 'E') for i in range(len(data))] \
           + [(len(data[0]) - 1, i, 'W') for i in range(len(data))] \
           + [(i, len(data) - 1, 'N') for i in range(len(data[0]))] \
           + [(i, 0, 'S') for i in range(len(data[0]))]
    maximum = 0
    for tup in dirs:
        visited.clear()
        energ = [[0 for _ in data[0]] for _ in data]
        energize(data, energ, tup[0], tup[1], tup[2])
        energized = sum(sum(r) for r in energ)
        maximum = max(maximum, energized)
    return maximum


def energize_no_recursion(board, energ, x, y, dir):
    next_t = (x, y, dir)
    stack = [next_t]
    while True:
        if not stack:
            return
        x, y, dir = stack.pop()
        if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board):
            continue
        if (x, y, dir) in visited:
            continue
        else:
            visited.add((x, y, dir))
        energ[y][x] = 1
        for to_dir in from_to[board[y][x]][dir]:
            next_dir = opposite[to_dir]
            stack.append((x + coord[next_dir][0], y + coord[next_dir][1], next_dir))


@timer
def part02_2(data):
    dirs =   [(0, i, 'E') for i in range(len(data))] \
           + [(len(data[0]) - 1, i, 'W') for i in range(len(data))] \
           + [(i, len(data) - 1, 'N') for i in range(len(data[0]))] \
           + [(i, 0, 'S') for i in range(len(data[0]))]
    maximum = 0
    for tup in dirs:
        visited.clear()
        energ = [[0 for _ in data[0]] for _ in data]
        energize_no_recursion(data, energ, tup[0], tup[1], tup[2])
        energized = sum(sum(r) for r in energ)
        maximum = max(maximum, energized)
    return maximum


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02_2(data))
