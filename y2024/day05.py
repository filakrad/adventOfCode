from utilities import timer


def add_to_dict_list(dct, key, value):
    if key in dct:
        dct[key].append(value)
    else:
        dct[key] = [value]


@timer
def parse(file_name):
    rules = dict()
    updates = []
    do_rules = True
    with open(file_name, "r") as f:
        for line in f.readlines():
            if not line.strip():
                do_rules = False
                continue
            if do_rules:
                k, v = line.strip().split("|")
                add_to_dict_list(rules, int(k), int(v))
            else:
                updates.append([int(x) for x in line.strip().split(",")])
    all_nums = set()
    for v in rules.values():
        for x in v:
            all_nums.add(x)
    for n in all_nums:
        if n not in rules:
            rules[n] = []
    return rules, updates


def is_correct(update, rules):
    for k, v in rules.items():
        if k not in update:
            continue
        for j in update[update.index(k):]:
            if j in rules:
                if k in rules[j]:
                    return False
    return True


@timer
def part01(data):
    rules, updates = data
    total = 0
    for up in updates:
        if is_correct(up, rules):
            middle_index = (len(up) - 1) // 2
            total += up[middle_index]
    return total


def correct_order(update, rules):
    corrected = []
    for u in update:
        index = 0
        for i, c in enumerate(corrected):
            if u in rules[c]:
                index = i + 1
            if c in rules[u]:
                break
        corrected.insert(index, u)
    return corrected


@timer
def part02(data):
    rules, updates = data
    total = 0
    for up in updates:
        if not is_correct(up, rules):
            corrected = correct_order(up, rules)
            middle_index = (len(corrected) - 1) // 2
            total += corrected[middle_index]
    return total


if __name__ == "__main__":
    data = parse("day05.txt")
    print(data)
    print(part01(data))
    print(part02(data))
