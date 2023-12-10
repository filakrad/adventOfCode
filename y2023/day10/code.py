import copy

from y2023.parser import load_rows_to_list
from y2023.utilities import timer


directions = "NESW"

coord = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}

opposite = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}

pipes = {
    '|': 'NS',
    "-": 'EW',
    'L': 'NE',
    'J': 'NW',
    'F': 'SE',
    '7': 'SW',
    '.': ''
}


@timer
def parse(file_name):
    data = load_rows_to_list(file_name)
    data = [row.strip() for row in data]
    return data


def replace_str_index(text,index=0,replacement=''):
    return f'{text[:index]}{replacement}{text[index+1:]}'


@timer
def part01(data):
    # find start
    all_starts = [(x, y) for y, row in enumerate(data) for x, symbol in enumerate(row) if symbol == 'S']
    start = all_starts[0]
    # find some next allowed pipe
    allowed = [d for d in directions if opposite[d] in pipes[data[start[1] + coord[d][1]][start[0] + coord[d][0]]]]
    direction = allowed[0]
    curr_pos = (start[0] + coord[direction][0], start[1] + coord[direction][1])
    # go along the pipe
    steps = 1
    while curr_pos != start:
        direction = pipes[data[curr_pos[1]][curr_pos[0]]].replace(opposite[direction], '')
        # data[curr_pos[1]] = replace_str_index(data[curr_pos[1]], curr_pos[0], '■')
        curr_pos = (curr_pos[0] + coord[direction][0], curr_pos[1] + coord[direction][1])
        steps += 1
    return steps // 2


right_sides = {
    '|': {'N': [(-1, 1), (-1, 0), (-1, -1)], 'S': [(1, 1), (1, 0), (1, -1)]},
    "-": {'W': [(-1, 1), (0, 1), (1, 1)], 'E': [(-1, -1), (0, -1), (1, -1)]},
    'L': {'N': [(-1, 1), (-1, 0), (-1, -1), (0, 1), (1, 1)], 'E': [(1, -1)]},
    'J': {'N':[(-1, -1)], 'W': [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]},
    'F': {'E': [(1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)], 'S': [(1, 1)]},
    '7': {'S': [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)], 'W': [(-1, 1)]}
}


@timer
def part02(data):
    # find start
    all_starts = [(x, y) for y, row in enumerate(data) for x, symbol in enumerate(row) if symbol == 'S']
    start = all_starts[0]

    # find some next allowed pipe
    allowed = [d for d in directions if opposite[d] in pipes[data[start[1] + coord[d][1]][start[0] + coord[d][0]]]]
    direction = allowed[0]
    curr_pos = (start[0] + coord[direction][0], start[1] + coord[direction][1])

    # trace pipe by '■'
    show_pipe = copy.deepcopy(data)
    show_pipe[start[1]] = replace_str_index(show_pipe[start[1]], start[0], '■')
    while curr_pos != start:
        direction = pipes[data[curr_pos[1]][curr_pos[0]]].replace(opposite[direction], '')
        show_pipe[curr_pos[1]] = replace_str_index(show_pipe[curr_pos[1]], curr_pos[0], '■')
        curr_pos = (curr_pos[0] + coord[direction][0], curr_pos[1] + coord[direction][1])

    #find some outer pipe
    start_row = len(data) // 2
    for i, c in enumerate(show_pipe[start_row]):
        if c == '■':
            break

    #replace 'S' pipe by correct piece
    start_piece = [k for k, v in pipes.items() if all(x in v for x in allowed)][0]
    data[start[1]] = replace_str_index(data[start[1]], start[0], start_piece)

    # wrap insides by I
    start = (i, start_row)
    direction = 'E' if data[start_row][i] == 'F' else 'N'
    curr_pos = (start[0] + coord[direction][0], start[1] + coord[direction][1])
    while curr_pos != start:
        symb = data[curr_pos[1]][curr_pos[0]]
        for p in right_sides[symb][opposite[direction]]:
            check = (curr_pos[0]+p[0], curr_pos[1]+p[1])
            if show_pipe[check[1]][check[0]] != '■':
                show_pipe[curr_pos[1]+p[1]] = replace_str_index(show_pipe[curr_pos[1]+p[1]], curr_pos[0]+p[0], 'I')
        direction = pipes[data[curr_pos[1]][curr_pos[0]]].replace(opposite[direction], '')
        curr_pos = (curr_pos[0] + coord[direction][0], curr_pos[1] + coord[direction][1])

    # Expand I's to whole insides
    for r, row in enumerate(show_pipe):
        replacing = False
        for i, c in enumerate(row):
            if c == 'I':
                replacing = True
            elif c == '■':
                replacing = False
            if replacing:
                row = replace_str_index(row, i, 'I')
        show_pipe[r] = row

    # count I's
    return sum(r.count('I') for r in show_pipe)


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))
