from utilities import timer
import re


@timer
def parse(file_name):
    with open(file_name, "r") as f:
        return f.read().strip()


@timer
def part01(data):
    total = 0
    muls = re.findall("mul\(\d+,\d+\)", data)
    for mul in muls:
        nums = re.findall("\d+", mul)
        total += int(nums[0]) * int(nums[1])
    return total


@timer
def part02(data):
    total = 0
    commands = re.findall("(mul\(\d+,\d+\))|(do\(\))|(don't\(\))", data)
    flag = True
    for comm in commands:
        if comm[0] and flag:
            nums = re.findall("\d+", comm[0])
            total += int(nums[0]) * int(nums[1])
        elif comm[1]:
            flag = True
        elif comm[2]:
            flag = False
    return total


if __name__ == "__main__":
    data = parse("day03.txt")
    print(part01(data))
    print(part02(data))
