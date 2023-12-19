import re

from y2023.utilities import timer


class Part:
    def __init__(self, text):
        tmp = re.findall(r'x=\d+|m=\d+|a=\d+|s=\d+', text)
        self.x = int(tmp[0][2:])
        self.m = int(tmp[1][2:])
        self.a = int(tmp[2][2:])
        self.s = int(tmp[3][2:])
        self.sum = self.x + self.m + self.a + self.s


class Rule:
    def __init__(self, text):
        self.ifs = text.split(',')

    def row(self, part):
        for i in self.ifs:
            splitted = i.split(':')
            if len(splitted) == 1:
                return splitted[0]
            elif '<' in splitted[0]:
                if part.__dict__[i[0]] < int(splitted[0][2:]):
                    return splitted[1]
            elif '>' in splitted[0]:
                if part.__dict__[i[0]] > int(splitted[0][2:]):
                    return splitted[1]
            elif '=' in splitted[0]:
                if part.__dict__[i[0]] == int(splitted[0][2:]):
                    return splitted[1]

    def from_to(self, the_dct):
        parted = []
        next_dct = {k: v for k, v in the_dct.items()}
        for i in self.ifs:
            splitted = i.split(':')
            if len(splitted) == 1:
                next_dct['next'] = splitted[0]
                parted.append(next_dct)
            elif '<' in splitted[0]:
                old = {k: v for k, v in next_dct.items()}
                to_split = old[i[0]]
                if to_split[1] < int(splitted[0][2:]):
                    continue
                old[i[0]] = (to_split[0], int(splitted[0][2:])-1)
                old['next'] = splitted[1]
                parted.append(old)
                next_dct[i[0]] = (int(splitted[0][2:]), to_split[1])
            elif '>' in splitted[0]:
                old = {k: v for k, v in next_dct.items()}
                to_split = old[i[0]]
                if to_split[0] > int(splitted[0][2:]):
                    continue
                old[i[0]] = (int(splitted[0][2:]) + 1, to_split[1])
                old['next'] = splitted[1]
                parted.append(old)
                next_dct[i[0]] = (to_split[0], int(splitted[0][2:]))
            elif '=' in splitted[0]:
                old1 = {k: v for k, v in next_dct.items()}
                old2 = {k: v for k, v in next_dct.items()}
                to_split = old1[i[0]]
                if not to_split[0] < int(splitted[0][2:]) < to_split[1]:
                    continue
                old1[i[0]] = (to_split[0], int(splitted[0][2:])-1)
                old1['next'] = splitted[1]
                parted.append(old1)
                old2[i[0]] = (int(splitted[0][2:]) + 1, to_split[1])
                old2['next'] = splitted[1]
                parted.append(old2)
                next_dct[i[0]] = (int(splitted[0][2:]), int(splitted[0][2:]))
        return parted





@timer
def parse(file_name):
    workflow = dict()
    parts = []
    with open(file_name, 'r') as f:
        x = f.read()
        work, parts_str = x.split('\n\n')
        for row in work.split('\n'):
            name, rules = row.split('{')
            rules = rules.replace('}', '')
            workflow[name] = Rule(rules)
        for row in parts_str.split('\n'):
            parts.append(Part(row))
    return workflow, parts



@timer
def part01(data):
    workflow, parts = data
    total = 0
    for part in parts:
        w_name = 'in'
        while w_name != 'R' and w_name != 'A':
            w_name = workflow[w_name].row(part)
        if w_name == 'A':
            total += part.sum
    return total



@timer
def part02(data):
    workflow, _ = data
    borders = {i: (1, 4000) for i in 'xmas'}
    borders['next'] = 'in'
    all_tests = [borders]
    total = 0
    while all_tests:
        testing = all_tests.pop()
        if testing['next'] == 'A':
            subtotal = 1
            for k, v in testing.items():
                if k == 'next':
                    continue
                subtotal *= v[1] - v[0] + 1
            total += subtotal
            continue
        elif testing['next'] == 'R':
            continue
        all_tests += workflow[testing['next']].from_to(testing)
        # print(all_tests)
        # break
    return total



if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))
