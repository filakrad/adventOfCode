from utilities import timer
from collections import Counter


@timer
def parse(file_name):
    l1 = []
    l2 = []
    with open(file_name, "r") as f:
        for line in f:
            nums = line.strip().split("   ")
            l1.append(int(nums[0]))
            l2.append(int(nums[1]))
    return l1, l2

@timer
def part01(data):
    list1, list2 = data
    list1.sort()
    list2.sort()
    dist = [abs(x[0] - x[1]) for x in zip(list1, list2)]
    return sum(dist)


@timer
def part02(data):
    list1, list2 = data
    list2_count = Counter(list2)
    total = 0
    for x in list1:
        total += x*list2_count[x]
    return total

if __name__ == "__main__":
    data = parse("day01.txt")
    print(part01(data))
    print(part02(data))
