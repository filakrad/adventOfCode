from days import parser
from days.utilities import timer

import numpy as np
from itertools import product


class SymmetryGroup:
    g1 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
    g2 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    g3 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])

    def __init__(self):
        self.elements = [self.g1, self.g2, self.g3]
        lng = 0
        while lng < len(self.elements):
            lng = len(self.elements)
            for a, b in product(list(self.elements), list(self.elements)):
                m = np.matmul(a, b)
                is_inside = any([(m == e).all() for e in self.elements])
                if not is_inside:
                    self.elements.append(m)


GROUP = SymmetryGroup()


class Scanner:
    def __init__(self, raw):
        self.name = raw[0]
        self.beacons = np.array([[int(x) for x in line.split(",")] for line in raw[1:]])

    def rotated_beacons(self, rotation):
        new_positions = []
        for b in self.beacons:
            new_vec = b.dot(rotation)
            new_positions.append(new_vec)
        return new_positions

    def __str__(self):
        return self.name + "\n" + "\n".join([str(x) for x in self.beacons])


def get_overlapping(b1, b2, l1=None, l2=None):
    overlap = []
    translation = tuple(b1[i]-b2[i] for i in range(3))
    for b in l2:
        tr_point = tuple(translation[i] + b[i] for i in range(3))
        # print(b ,tr_point)
        if tr_point in l1:
        # if any([(tr_point == e).all() for e in l1]):
            overlap.append([tr_point])
    return overlap


def get_new_translated_points(b1, b2, l2):
    new_points = []
    for b in l2:
        new_points.append(tuple(b1[i] - b2[i] + b[i] for i in range(3)))
    return new_points


def test_scanner(refferential, other):
    for h, rot in enumerate(GROUP.elements):
        new_points = other.rotated_beacons(rot)
        new_points = {tuple(x) for x in new_points}
        # print(new_points)
        for b1 in refferential:
            for b2 in new_points:
                overlap = get_overlapping(b1, b2, refferential, new_points)
                # if len(overlap) > 1:
                #     print(overlap)
                if len(overlap) >= 12:
                    print(overlap)
                    scanner = tuple(b1[i] - b2[i] for i in range(3))
                    points = get_new_translated_points(b1, b2, new_points)
                    return scanner, points
        # print(h, "\n", rot)
    return None, None


def max_distance(all_positions):
    dist = 0
    for p, q in product(all_positions, all_positions):
        d = sum([abs(p[i] - q[i]) for i in range(3)])
        dist = max(dist, d)
    return dist


@timer
def part01(data):
    refferential_scanner = data.pop(1)
    all_points = {tuple(x) for x in refferential_scanner.beacons}
    while data:
        print(len(data))
        tested_scanner = data.pop(0)
        print(tested_scanner.name)
        scanner, new_points = test_scanner(all_points, tested_scanner)
        if new_points is not None:
            all_points = all_points.union(new_points)
            print(scanner)
        else:
            data.append(tested_scanner)
        print(len(all_points))
    return len(all_points)


@timer
def part02(data):
    all_scanner_positions = [(0, 0, 0)]
    refferential_scanner = data.pop(1)
    all_points = {tuple(x) for x in refferential_scanner.beacons}
    while data:
        print(len(data))
        tested_scanner = data.pop(0)
        print(tested_scanner.name)
        scanner, new_points = test_scanner(all_points, tested_scanner)
        if new_points is not None:
            all_points = all_points.union(new_points)
            all_scanner_positions.append(scanner)
        else:
            data.append(tested_scanner)
        print(len(all_points))
    print(all_scanner_positions)
    return max_distance(all_scanner_positions)


@timer
def load_data():
    raw = parser.load_blocks("day19.txt", "\n")
    scanners = []
    for r in raw:
        scanners.append(Scanner(r))
    return scanners



@timer
def main():
    data = load_data()
    print(part01(data))
    print(part02(data))


if __name__ == "__main__":
    main()