from itertools import product
import math

from days import parser
from days.utilities import timer


class Reactor:
    def __init__(self, data):
        self.on_cubes = set()
        self.instructions = data

    def do_instructions(self):
        for switch, coords in self.instructions:
            if not self.check_eligibility(coords):
                continue
            if switch:
                self.turn_on(coords)
            else:
                self.turn_off(coords)

    @staticmethod
    def get_triples(coords):
        ranges = [range(x[0], x[1]+1) for x in coords]
        return product(*ranges)

    def turn_off(self, coords):
        triples = self.get_triples(coords)
        for triple in triples:
            self.on_cubes.discard(triple)

    def turn_on(self, coords):
        triples = self.get_triples(coords)
        for triple in triples:
            self.on_cubes.add(triple)

    def check_eligibility(self, coords):
        for c in coords:
            if c[1] < -55 or c[0] > 55:
                return False
        return True


class Reactor2(Reactor):
    def __init__(self, data):
        self.on_regions = set()
        self.instructions = self.transform_to_halfopen(data)

    def transform_to_halfopen(self, data):
        transformed = []
        for s, c in data:
            transformed.append((s, tuple([(i[0], i[1]+1) for i in c])))
        return transformed

    def do_instructions(self):
        num_instructions = len(self.instructions)
        cnt = 0
        for switch, coord in self.instructions:
            cnt += 1
            print(coord, len(self.on_regions))
            to_remove = set()
            for reg in self.on_regions:
                if self.is_cube_intersect(reg, coord):
                    to_remove.add(reg)
            if len(to_remove) > 10:

                print("before_glue", len(self.on_regions))
                self.on_regions = self.glue_back(self.on_regions)
                print("after_glue", len(self.on_regions))
                to_remove = set()
                for reg in self.on_regions:
                    if self.is_cube_intersect(reg, coord):
                        to_remove.add(reg)

            for rem in to_remove:
                self.on_regions.remove(rem)
            print(len(to_remove))

            if coord == ((-49, 0), (-11, 43), (-10, 39)):
                print("\n".join(str(x) for x in to_remove))

            if switch:
                to_add = list(to_remove)
                to_add.append(coord)
                new = True
                while new:
                    for i, c1 in enumerate(to_add):
                        new = {}
                        for c2 in to_add[i + 1:]:
                            if self.is_cube_intersect(c1, c2):
                                new = self.split_cubes(c1, c2, switch)
                                to_add.remove(c1)
                                to_add.remove(c2)
                                to_add += list(new)
                                to_add = list(self.glue_back(to_add))
                                break
                        if new:
                            break
                self.on_regions = self.on_regions.union(set(to_add))
            else:
                for r in to_remove:
                    splitted = self.split_cubes(r, coord, switch)
                    self.on_regions = self.on_regions.union(splitted)

            if self.test_correctness():
                print(to_remove)
                print(coord)
                break

            print(f"finished {cnt}/{num_instructions}")

    def test_correctness(self):
        regs = list(self.on_regions)
        error = False
        for i, c1 in enumerate(regs):
            for c2 in regs[i+1:]:
                if self.is_cube_intersect(c1, c2):
                    error = True
                    print("error", c1, c2)
        return error

    def split_cubes(self, c1, c2, switch):
        edges = [sorted([c1[i][0], c1[i][1], c2[i][0], c2[i][1]]) for i in range(3)]
        edges = [[(e[i], e[i+1]) for i in range(3)] for e in edges]
        sub_cubes = product(*edges)
        on_sub_cubes = set()
        for sc in sub_cubes:
            if switch:
                if self.is_cube_inside_cube(sc, c1) or self.is_cube_inside_cube(sc, c2):
                    on_sub_cubes.add(sc)
            else:
                if self.is_cube_inside_cube(sc, c1) and not self.is_cube_inside_cube(sc, c2):
                    on_sub_cubes.add(sc)
        on_sub_cubes = self.remove_size_0(on_sub_cubes)
        on_sub_cubes = self.glue_back(on_sub_cubes)
        return on_sub_cubes

    @staticmethod
    def glue_back(cubes):
        last_size = 0
        cubes = list(cubes)
        while len(cubes) != last_size:
            last_size = len(cubes)
            for i, c1 in enumerate(cubes):
                br = False
                for c2 in cubes[i + 1:]:
                    if c1[0] == c2[0] and c1[1] == c2[1] and c1[2][1] == c2[2][0]:
                        new_cube = (c1[0], c1[1], (c1[2][0], c2[2][1]))
                        cubes.remove(c1)
                        cubes.remove(c2)
                        cubes.append(new_cube)
                        br = True
                        break
                    elif c1[0] == c2[0] and c1[1][1] == c2[1][0] and c1[2] == c2[2]:
                        new_cube = (c1[0], (c1[1][0], c2[1][1]), c1[2])
                        cubes.remove(c1)
                        cubes.remove(c2)
                        cubes.append(new_cube)
                        br = True
                        break
                    elif c1[0][1] == c2[0][0] and c1[1] == c2[1] and c1[2] == c2[2]:
                        new_cube = ((c1[0][0], c2[0][1]), c1[1], c1[2])
                        cubes.remove(c1)
                        cubes.remove(c2)
                        cubes.append(new_cube)
                        br = True
                        break
                if br:
                    break
        return set(cubes)


    @staticmethod
    def remove_size_0(cubes):
        real_cubes = set()
        for c in cubes:
            if all([coord[1] - coord[0] > 0 for coord in c]):
                real_cubes.add(c)
        return real_cubes

    @staticmethod
    def is_cube_inside_cube(c1, c2):
        return all(c1[i][0] >= c2[i][0] and c1[i][1] <= c2[i][1] for i in range(3))

    @staticmethod
    def is_cube_intersect(c1, c2):
        return all(c1[i][0] <= c2[i][0] < c1[i][1]
                   or c1[i][0] < c2[i][1] <= c1[i][1]
                   or c2[i][0] <= c1[i][0] < c2[i][1]
                   or c2[i][0] < c1[i][1] <= c2[i][1] for i in range(3))

    def number_on(self):
        total = 0
        for reg in self.on_regions:
            sizes = [i[1] - i[0] for i in reg]
            total += math.prod(sizes)
        return total



@timer
def part01(data):
    reactor = Reactor(data)
    reactor.do_instructions()
    return len(reactor.on_cubes)


@timer
def part02(data):
    reactor = Reactor2(data)
    reactor.do_instructions()
    print(len(reactor.on_regions))
    return reactor.number_on()


def parse_row(row):
    switch, coordinates = row.strip().split(" ")
    switch = 1 if switch == "on" else 0
    coordinates = coordinates.replace("=", "").replace("y", "").replace("z", "").replace("x", "")
    coordinates = coordinates.split(",")
    coordinates = [[int(x) for x in c.split("..")] for c in coordinates]
    return switch, coordinates


@timer
def load_data():
    return parser.load_rows_to_list("day22.txt", parse_row)


@timer
def main():
    data = load_data()
    print(part01(data))
    print(part02(data))


if __name__ == "__main__":
    main()