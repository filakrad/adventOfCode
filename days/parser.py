def empty_function(x, **kwargs):
    return x


def string_without_newline(line, **kwargs):
    return line[:-1]


def delimited_values(row, delimiter=",", functions=[]):
    splitted = row.split(delimiter)
    return tuple(f(x) for f, x in zip(functions, splitted))


def load_rows_to_list(file_name, parse_function=empty_function, **kwargs):
    out_list = []
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            out_list.append(parse_function(line, **kwargs))
            line = f.readline()
    return out_list


def load_bingo_cards(file_name):
    cards = []
    with open(file_name, "r") as f:
        header = f.readline()
        header = header.split(",")
        header = [int(x) for x in header]
        line = f.readline()
        card = []
        while line:
            line = f.readline()
            splitted = line.split()
            if not splitted:
                cards.append(card)
                card = []
            card += [int(x) for x in splitted]
    return header, cards


def parse_two_times(row, delim1="->", delim2=",", func=int):
    stage1 = row.split(delim1)
    out = []
    for part in stage1:
        out.append(tuple([func(x) for x in part.split(delim2)]))
    return out


def load_two_things(file_name, function1, delimiter, function2):
    list1 = []
    list2 = []
    first_part = True
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            if line == delimiter:
                first_part = False
            elif first_part:
                list1.append(function1(line))
            else:
                list2.append(function2(line))
            line = f.readline()
    return list1, list2


def load_one_row(file_name, parse_function=empty_function):
    with open(file_name, "r") as f:
        line = f.readline()
        return parse_function(line)
