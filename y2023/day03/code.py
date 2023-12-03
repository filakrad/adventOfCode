import re
import string

from y2023.parser import load_rows_to_list
from y2023.utilities import timer


class Schematic:
    def __init__(self, data):
        self.data = data
        self.y_size = len(data)
        self.x_size = len(data[0])

    def get_rectangle(self, line, x0, x1):
        x_range = range(x0-1, x1+1)
        y_range = range(line - 1, line + 2)
        return [(x, y) for x in x_range for y in y_range if 0 <= x < self.x_size and 0 <= y < self.y_size]

    @timer
    def part01(self):
        allowed_symbols = string.digits + "."
        total = 0
        for i, row in enumerate(data):
            nums = re.finditer("[0-9]+", row)
            for num in nums:
                rect = self.get_rectangle(i, num.span()[0], num.span()[1])
                if any(self.data[y][x] not in allowed_symbols for x, y in rect):
                    total += int(num.group())
        return total

    @timer
    def part02(self):
        total = 0
        all_numbers = []
        for i, row in enumerate(data):
            nums = re.finditer("[0-9]+", row)
            all_numbers += [(i, n.span(), int(n.group())) for n in nums] # (y, xrange, number)
        for i, row in enumerate(self.data):
            stars = re.finditer("\*", row)
            for star in stars:
                rect = self.get_rectangle(i, star.span()[0], star.span()[1])
                digits = [x for x in rect if self.data[x[1]][x[0]].isdigit()]
                the_nums = set()
                for digit in digits:
                    the_nums.add(next(num for num in all_numbers if digit[1] == num[0] and digit[0] in range(num[1][0], num[1][1] + 1)))
                if len(the_nums) == 2:
                    nums_list = list(the_nums)
                    total += nums_list[0][2] * nums_list[1][2]
        return total


if __name__ == "__main__":
    data = load_rows_to_list("data.txt")
    data = [row.strip() for row in data]
    schem = Schematic(data)
    print(data)
    print(schem.part01())
    print(schem.part02())