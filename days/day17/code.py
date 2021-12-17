from days import parser
from days.utilities import timer


class Target:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range

    def is_behind(self, item):
        return item[0] < self.x_range[1] and item[1] > self.y_range[0]

    def __contains__(self, item):
        return self.x_range[0] <= item[0] <= self.x_range[1] and self.y_range[0] <= item[1] <= self.y_range[1]


class Shot:
    def __init__(self, x, y, target):
        self.pos_x = 0
        self.pos_y = 0
        self.speed_x = x
        self.speed_y = y
        self.target = target
        self.max_y = 0

    def step(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.speed_x = max(0, self.speed_x - 1)
        self.speed_y -= 1
        self.max_y = max(self.max_y, self.pos_y)

    def is_on_target(self):
        while self.target.is_behind((self.pos_x, self.pos_y)):
            self.step()
            if (self.pos_x, self.pos_y) in self.target:
                return True
        return False


@timer
def part01(x_range, y_range):
    target = Target(x_range, y_range)
    max_y = 0
    for x in range(x_range[1]):
        for y in range(abs(y_range[0])):
            shot = Shot(x, y, target)
            if shot.is_on_target():
                max_y = max(max_y, shot.max_y)
    return max_y


@timer
def part02(x_range, y_range):
    target = Target(x_range, y_range)
    possibilities = 0
    for x in range(x_range[1]+1):
        for y in range(y_range[0]-1, abs(y_range[0])+1):
            shot = Shot(x, y, target)
            if shot.is_on_target():
                possibilities += 1
    return possibilities


@timer
def load_data():
    row = parser.load_one_row("day17.txt", lambda line: line.strip())
    x, y = row.split(" ")[-2], row.split(" ")[-1]
    x = x.strip(",").split("=")[-1].split("..")
    y = y.strip(",").split("=")[-1].split("..")
    x = [int(i) for i in x]
    y = [int(i) for i in y]
    return x, y


@timer
def main():
    x_range, y_range = load_data()
    print(x_range, y_range)
    print(part01(x_range, y_range))
    print(part02(x_range, y_range))


if __name__ == "__main__":
    main()
