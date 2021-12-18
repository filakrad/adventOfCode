from days import parser
from days.utilities import timer

import ast
import itertools

neighbor = None


class Number:
    def __init__(self, x, depth=0, parent=None, initial=False):
        self.depth = depth
        self.sub_numbers = []
        if type(x) is list:
            self.type = 0
            self.sub_numbers = [Number(x[0], depth+1, self, initial), Number(x[1], depth+1, self, initial)]
        else:
            self.type = 1
            self.left_neighbor = None
            self.right_neighbor = None
            if initial:
                self.set_neighbors()
        self.parent = parent
        self.value = [x.value for x in self.sub_numbers] if self.type == 0 else x
        self.exploded = False
        self.substitute = None
        self.splitted = False

    def set_neighbors(self):
        global neighbor
        self.left_neighbor = neighbor
        self.right_neighbor = None
        if neighbor is not None:
            neighbor.right_neighbor = self
        neighbor = self

    def __str__(self):
        return str(self.value)

    def reduce(self):
        while True:
            self.fix_value()
            x = self.do_all_explosions()
            if x:
                continue
            x = self.do_all_splits()
            if x:
                continue
            break

    def do_all_explosions(self):
        if self.type == 0 and self.depth >= 4:
            self.explode()
            return True
        else:
            for i, sub in enumerate(self.sub_numbers):
                end = sub.do_all_explosions()
                if end:
                    return True
        return False


    def do_all_splits(self):
        if self.type == 1 and self.value >= 10:
            self.split()
            return True
        else:
            for i, sub in enumerate(self.sub_numbers):
                end = sub.do_all_splits()
                if end:
                    return True
        return False

    def fix_value(self):
        for i in self.sub_numbers:
            i.fix_value()
        self.value = [x.value for x in self.sub_numbers] if self.type == 0 else self.value

    def explode(self):
        self.exploded = True
        new_number = Number(0, self.depth, self.parent)
        new_number.left_neighbor = self.sub_numbers[0].left_neighbor
        new_number.right_neighbor = self.sub_numbers[1].right_neighbor
        idx = self.parent.sub_numbers.index(self)
        self.parent.sub_numbers[idx] = new_number
        if (left := self.sub_numbers[0].left_neighbor) is not None:
            left.value += self.sub_numbers[0].value
            left.right_neighbor = new_number
        if (right := self.sub_numbers[1].right_neighbor) is not None:
            right.value += self.sub_numbers[1].value
            right.left_neighbor = new_number
        self.substitute = new_number


    def split(self):
        self.splitted = True
        left_val = self.value // 2
        right_val = self.value - left_val
        num = [left_val, right_val]
        new_number = Number(num, self.depth, self.parent)
        new_number.sub_numbers[0].left_neighbor = self.left_neighbor
        new_number.sub_numbers[0].right_neighbor = new_number.sub_numbers[1]
        new_number.sub_numbers[1].left_neighbor = new_number.sub_numbers[0]
        new_number.sub_numbers[1].right_neighbor = self.right_neighbor
        if self.left_neighbor is not None:
            self.left_neighbor.right_neighbor = new_number.sub_numbers[0]
        if self.right_neighbor is not None:
            self.right_neighbor.left_neighbor = new_number.sub_numbers[1]
        self.substitute = new_number
        idx = self.parent.sub_numbers.index(self)
        self.parent.sub_numbers[idx] = new_number

    def magnitude(self):
        if self.type == 1:
            return self.value
        return 3*self.sub_numbers[0].magnitude() + 2*self.sub_numbers[1].magnitude()

def add_numbers(x, y):
    return [x, y]


def action_test(x, depth):
    if type(x) is list:
        if depth >= 4:
            print("explosion", x, depth)
            return 1
        else:
            return 0
    else:
        if x >= 10:
            print("split", x)
            return 2
        else:
            return 0


def reduce_number(x, depth=0):
    # if action_test(x, depth):

    if type(x[0]) is list and depth < 4:
        print(True)
        reduce_number(x[0], depth+1)
    else:
        print(False)


@timer
def part01(data):
    final_num = data[0]
    for a in data[1:]:
        num = add_numbers(final_num, a)
        num = Number(num, initial=True)
        num.reduce()
        final_num = ast.literal_eval(str(num))
    final = Number(final_num, initial=True)
    return final.magnitude()


@timer
def part02(data):
    current_max = 0
    all_pairs = itertools.product(data, data)
    # print(len(list(all_pairs)))
    for i, p in enumerate(all_pairs):
        num = add_numbers(p[0], p[1])
        num = Number(num, initial=True)
        num.reduce()
        current_max = max(num.magnitude(), current_max)
    return current_max


@timer
def load_data():
    return parser.load_rows_to_list("day18.txt", lambda line: ast.literal_eval(line) )


@timer
def main():
    data = load_data()
    # print(data)
    print(part01(data))
    print(part02(data))


if __name__ == "__main__":
    main()