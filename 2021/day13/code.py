from days import parser
from days.utilities import timer


class Paper:
    def __init__(self, ones):
        self.max_x = max([x[0] for x in ones]) + 1
        self.max_y = max([x[1] for x in ones]) + 1
        self.grid = [[0 for _ in range(self.max_x)] for _ in range(self.max_y)]
        for p in ones:
            self.grid[p[1]][p[0]] = 1

    def fold(self, x=None, y=None):
        new_max_y = self.max_y
        new_max_x = self.max_x
        if x is None:
            x = self.max_x
            new_max_y = (self.max_y - 1) // 2
        if y is None:
            y = self.max_y
            new_max_x = (self.max_x - 1) // 2

        new_grid = [[0 for _ in range(new_max_x)] for _ in range(new_max_y)]

        for i in range(self.max_y):
            for j in range(self.max_x):
                if i == y or j == x:
                    continue
                new_grid[y-abs(y-i)][x - abs(x-j)] = max(new_grid[y-abs(y-i)][x - abs(x-j)], self.grid[i][j])

        self.max_x = new_max_x
        self.max_y = new_max_y
        self.grid = new_grid

    def fold_all(self, folds):
        for f in folds:
            fd= {f[0]: f[1]}
            self.fold(**fd)
        return sum([sum(l) for l in self.grid])

    def __str__(self):
        return "\n".join(["".join([" " if x == 0 else "#" for x in line]) for line in self.grid])


@timer
def part01(ones, folds):
    paper = Paper(ones)
    return paper.fold_all(folds[:1])


@timer
def part02(ones, folds):
    paper = Paper(ones)
    paper.fold_all(folds)
    return paper


@timer
def load_data():
    d1, d2 = parser.load_two_things("day13.txt",
                                    lambda line: [int(x) for x in line.strip().split(",")],
                                    "\n",
                                    lambda line: line.strip().split()[-1].split("="))
    d2 = [(x[0], int(x[1])) for x in d2]
    return d1, d2



@timer
def main():
    ones, folds = load_data()
    print(ones, folds)
    print(part01(ones, folds))
    print(part02(ones, folds))


if __name__ == "__main__":
    main()
