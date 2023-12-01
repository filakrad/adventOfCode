from y2023.parser import load_rows_to_list
from y2023.utilities import timer


@timer
def part01(data):
    sum = 0
    for row in data:
        digits = [x for x in row if x.isdigit()]
        num = digits[0] + digits[-1]
        sum += int(num)
    return sum


string_digits = {"one": "1",
                 "two": "2",
                 "three": "3",
                 "four": "4",
                 "five": "5",
                 "six": "6",
                 "seven": "7",
                 "eight": "8",
                 "nine": "9"}


@timer
def part02(data):
    sum = 0
    for row in data:
        digits = [(i, x) for i, x in enumerate(row) if x.isdigit()]
        digits += [(row.find(k), v) for k, v in string_digits.items() if row.find(k) != -1]
        digits += [(row.rfind(k), v) for k, v in string_digits.items() if row.rfind(k) != -1]
        digits.sort(key=lambda x: x[0])
        num = int(digits[0][1] + digits[-1][1])
        sum += num
    return sum


if __name__ == "__main__":
    data = load_rows_to_list("data01.txt")
    print(part01(data))
    print(part02(data))
