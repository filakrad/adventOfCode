from days import parser

def part01(data):
    total_unique = 0
    for d in data:
        total_unique += sum([len(i) in [2, 3, 4, 7] for i in d[1]])
    return total_unique

class Display:
    def __init__(self, scrambled):
        self.scrambled = scrambled
        self.lengths = {len(i): i for i in self.scrambled}
        self.correct_mapping = {i: None for i in range(1, 8)}
        self.deduce()

    def deduce(self):
        self.deduce_1()
        self.deduce_2()

    def deduce_1(self):
        for ch in self.lengths[3]:
            if ch not in self.lengths[2]:
                self.correct_mapping[1] = ch

    def deduce_1(self):
        for ch in self.lengths[3]:
            if ch not in self.lengths[2]:
                self.correct_mapping[1] = ch


if __name__ == "__main__":
    data = parser.load_rows_to_list("day08.txt", parse_function=parser.parse_two_times, delim1=" | ", delim2=" ",
                                    func=str.strip)
    print(part01(data))