from days import parser


def part01(data):
    total_unique = 0
    for d in data:
        total_unique += sum([len(i) in [2, 3, 4, 7] for i in d[1]])
    return total_unique


class Display:
    numbers = {(1, 2, 3, 4, 5, 6): 0,
               (2, 3): 1,
               (1, 2, 4, 5, 7): 2,
               (1, 2, 3, 4, 7): 3,
               (2, 3, 6, 7): 4,
               (1, 3, 4, 6, 7): 5,
               (1, 3, 4, 5, 6, 7): 6,
               (1, 2, 3): 7,
               (1, 2, 3, 4, 5, 6, 7): 8,
               (1, 2, 3, 4, 6, 7): 9
               }

    def __init__(self, scrambled):
        self.scrambled_input = scrambled[0]
        self.lengths = {len(i): list() for i in self.scrambled_input}
        for num in self.scrambled_input:
            self.lengths[len(num)].append(num)
        self.segment_counts = self.get_segment_counts()
        self.segments = {i: None for i in range(1, 8)}
        self.deduce_segments()
        self.reversed_segments = {x: y for y, x in self.segments.items()}
        self.out = [self.deduce_number(x) for x in scrambled[1]]

    def deduce_number(self, scrambled_num):
        segs = sorted([self.reversed_segments[i] for i in scrambled_num])
        return self.numbers[tuple(segs)]

    def deduce_segments(self):
        self.deduce_segment_1()
        self.deduce_segment_3()
        self.deduce_segment_5()
        self.deduce_segment_6()
        self.deduce_segment_2()
        self.deduce_segment_7()
        self.deduce_segment_4()

    def deduce_segment_1(self):
        for ch in self.lengths[3][0]:
            if ch not in self.lengths[2][0]:
                self.segments[1] = ch

    def deduce_segment_3(self):
        self.segments[3] = [ch for ch, c in self.segment_counts.items() if c == 9][0]

    def deduce_segment_5(self):
        self.segments[5] = [ch for ch, c in self.segment_counts.items() if c == 4][0]

    def deduce_segment_6(self):
        self.segments[6] = [ch for ch, c in self.segment_counts.items() if c == 6][0]

    def deduce_segment_2(self):
        self.segments[2] = [ch for ch in self.lengths[2][0] if ch != self.segments[3]][0]

    def deduce_segment_7(self):
        len_4_5 = self.lengths[4] + self.lengths[5]
        totals = {ch: 0 for ch in self.lengths[7][0]}
        for ch in totals.keys():
            for x in len_4_5:
                if ch in x:
                    totals[ch] += 1
        self.segments[7] = [ch for ch, i in totals.items() if i == 4][0]

    def deduce_segment_4(self):
        self.segments[4] = [ch for ch in self.lengths[7][0] if ch not in self.segments.values()][0]

    def get_segment_counts(self):
        totals = {ch: 0 for ch in self.lengths[7][0]}
        for ch in totals.keys():
            for scr in self.scrambled_input:
                if ch in scr:
                    totals[ch] += 1
        return totals

def part02(data):
    total = 0
    for d in data:
        disp = Display(d).out
        total += 1000*disp[0] + 100*disp[1] + 10*disp[2] + disp[3]
    return total


if __name__ == "__main__":
    data = parser.load_rows_to_list("day08.txt", parse_function=parser.parse_two_times, delim1=" | ", delim2=" ",
                                    func=str.strip)
    print(part01(data))
    print(part02(data))