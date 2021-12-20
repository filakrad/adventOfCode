from days import parser
from days.utilities import timer


class Picture:
    def __init__(self, alg, pic, padding=0):
        self.algorithm = alg
        self.picture = pic
        self.padding = padding
        self.picture = self.pad_pic()

    def __str__(self):
        return "\n".join(["".join(["#" if x == 1 else " " for x in line]) for line in self.picture])

    def do_algorithm(self):
        bigger_pic = self.pad_pic()
        new_pic = [[0 for x in line] for line in bigger_pic]
        for r in range(1, len(bigger_pic)-1):
            for c in range(1, len(bigger_pic[0])-1):
                num = bigger_pic[r-1][c-1:c+2] + bigger_pic[r][c-1:c+2] + bigger_pic[r+1][c-1:c+2]
                int_num = sum([x*(2**i) for i, x in enumerate(reversed(num))])
                new_pic[r][c] = self.algorithm[int_num]
        next_padding = self.algorithm[0] if self.padding == 0 else self.algorithm[-1]
        new_pic = self.remove_padding(new_pic)
        return Picture(self.algorithm, new_pic, next_padding)

    def remove_padding(self, new_pic):
        return [[new_pic[r][x] for x in range(1, len(new_pic[0])-1)] for r in range(1, len(new_pic)-1)]

    def pad_pic(self):
        bigger = [[self.padding for _ in range(len(self.picture[0]) + 2)]]
        for line in self.picture:
            bigger.append([self.padding] + line + [self.padding])
        bigger.append([self.padding for _ in range(len(self.picture[0])+2)])
        return bigger

    def get_num_lights(self):
        return sum([sum(row) for row in self.picture])


@timer
def part01(algorithm, start_picture):
    pic = Picture(algorithm, start_picture)
    for _ in range(2):
        pic = pic.do_algorithm()
    return pic.get_num_lights()


@timer
def part02(algorithm, start_picture):
    pic = Picture(algorithm, start_picture)
    for _ in range(50):
        pic = pic.do_algorithm()
    return pic.get_num_lights()


@timer
def load_data():
    alg, pic = parser.load_two_things("day20.txt",
                                      lambda line: [1 if x == "#" else 0 for x in line.strip()],
                                      "\n",
                                      lambda line: [1 if x == "#" else 0 for x in line.strip()])
    return alg[0], pic


@timer
def main():
    algorithm, start_picture = load_data()
    print(part01(algorithm, start_picture))
    print(part02(algorithm, start_picture))


if __name__ == "__main__":
    main()
