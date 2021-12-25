from days import parser
from days.utilities import timer


class Floor:
    def __init__(self, data):
        self.eastbound = set()
        self.southbound = set()
        self.east_max = len(data[0])
        self.south_max = len(data)
        for i, row in enumerate(data):
            for j, cuc in enumerate(row):
                if cuc == ">":
                    self.eastbound.add((j, i))
                elif cuc == "v":
                    self.southbound.add((j, i))

    def move_east(self):
        movables = set()
        for cuc in self.eastbound:
            next_pos = (((cuc[0] + 1) % self.east_max), cuc[1])
            if next_pos not in self.eastbound and next_pos not in self.southbound:
                movables.add((cuc, next_pos))
        for pos in movables:
            self.eastbound.remove(pos[0])
            self.eastbound.add(pos[1])
        return len(movables)

    def move_south(self):
        movables = set()
        for cuc in self.southbound:
            next_pos = (cuc[0], ((cuc[1] + 1) % self.south_max))
            if next_pos not in self.eastbound and next_pos not in self.southbound:
                movables.add((cuc, next_pos))
        for pos in movables:
            self.southbound.remove(pos[0])
            self.southbound.add(pos[1])
        return len(movables)

    def count_steps(self):
        steps = 0
        while True:
            east_steps = self.move_east()
            south_steps = self.move_south()
            steps += 1
            if east_steps + south_steps == 0:
                break
        return steps





@timer
def part01(data):
    sea_floor = Floor(data)
    return sea_floor.count_steps()


@timer
def part02(data):
    pass


@timer
def load_data():
    return parser.load_rows_to_list("day25.txt", lambda row: row.strip())


@timer
def main():
    data = load_data()
    print(part01(data))
    print(part02(data))


if __name__ == "__main__":
    main()