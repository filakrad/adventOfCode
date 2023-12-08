import math

from y2023.utilities import timer


@timer
def parse(file_name):
    nodes = dict()
    with open(file_name, "r") as f:
        tape = f.readline().strip()
        f.readline()
        line = f.readline()
        while line:
            key, vals = line.split('=')
            vals = vals.split(",")
            nodes[key.strip()] = {'L': vals[0][2:], 'R':vals[1][1:4]}
            line = f.readline()
    return tape, nodes


@timer
def part01(data):
    curr_node = 'AAA'
    steps = 0
    tape, nodes = data
    tape_length = len(tape)
    while curr_node != 'ZZZ':
        symbol = tape[steps % tape_length]
        steps += 1
        curr_node = nodes[curr_node][symbol]
    return steps


@timer
def part02_too_long(data):
    steps = 0
    tape, nodes = data
    curr_nodes = [k for k in nodes.keys() if k[-1] == 'A']
    tape_length = len(tape)

    while not all(n[-1] == 'Z' for n in curr_nodes):
        symbol = tape[steps % tape_length]
        steps += 1
        curr_nodes = [nodes[node][symbol] for node in curr_nodes]
    return steps


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def find_common_end(a, b):
    curr_a = a["start"]
    curr_b = b["start"]
    while curr_a != curr_b:
        if curr_a < curr_b:
            curr_a += a["cycle"]
        else:
            curr_b += b["cycle"]
    return {"start": curr_a, "cycle": lcm(a["cycle"], b["cycle"])}


@timer
def part02(data):
    tape, nodes = data
    start_nodes = [k for k in nodes.keys() if k[-1] == 'A']
    tape_length = len(tape)

    cycles = []

    for node in start_nodes:
        z_nodes = []
        curr_node = node
        steps = 0
        while len(z_nodes) < 2:
            symbol = tape[steps % tape_length]
            steps += 1
            curr_node = nodes[curr_node][symbol]
            if curr_node[-1] == 'Z':
                z_nodes.append(steps)
        cycles.append({"start": z_nodes[0], "cycle": z_nodes[1] - z_nodes[0]})

    while len(cycles) > 1:
        new = find_common_end(cycles.pop(0), cycles.pop(0))
        cycles.append(new)

    return cycles[0]["start"]


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))