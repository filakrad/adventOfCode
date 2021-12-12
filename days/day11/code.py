from days import parser
from days.utilities import timer


class Grid:
    neighbors = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
    neighbors.remove((0, 0))

    def __init__(self, octopussies):
        self.octopussies = octopussies
        self.flash_positions = []
        self.max_y = len(self.octopussies) - 1
        self.max_x = len(self.octopussies[0]) - 1
        self.flash_counter = 0

    def do_step(self):
        for y, row in enumerate(self.octopussies):
            for x, octo in enumerate(row):
                self.add_energy_and_flash_check(x, y)
        while self.flash_positions:
            tmp_flash_positions = self.flash_positions
            self.flash_positions = []
            for pos in tmp_flash_positions:
                for x, y in self.neighbors:
                    if 0 <= (cx := pos[0] + x) <= self.max_x and 0 <= (cy := pos[1] + y) <= self.max_y:
                        self.add_energy_and_flash_check(cx, cy)
        self.remove_flashed()

    def add_energy_and_flash_check(self, x, y):
        self.octopussies[y][x].add_energy()
        if self.octopussies[y][x].is_flash():
            self.flash_counter += 1
            self.flash_positions.append((x, y))

    def remove_flashed(self):
        for row in self.octopussies:
            for octo in row:
                octo.flashed = False

    def __str__(self):
        return "\n".join(["".join([str(x) for x in row]) for row in self.octopussies]) + "\n"


class Octopus:
    def __init__(self, energy):
        self.energy = energy
        self.flashed = False

    def add_energy(self):
        if self.flashed:
            return
        self.energy += 1

    def is_flash(self):
        if self.energy > 9:
            self.energy = 0
            self.flashed = True
            return True
        return False

    def __str__(self):
        return str(self.energy)


class Grid2(Grid):
    def is_synchronised(self):
        for row in self.octopussies:
            for octo in row:
                if octo.energy != 0:
                    return False
        return True


@timer
def part01(data):
    grid = Grid(data)
    for _ in range(100):
        grid.do_step()
    return grid.flash_counter


@timer
def part02(data):
    grid = Grid2(data)
    iteration = 0
    while not grid.is_synchronised():
        grid.do_step()
        iteration += 1
    return iteration


@timer
def load_data():
    return parser.load_rows_to_list("day11.txt", lambda row: [Octopus(int(x)) for x in row.strip()])


@timer
def main():
    data = load_data()
    print(part01(data))
    data = load_data()
    print(part02(data))


if __name__ == "__main__":
    main()