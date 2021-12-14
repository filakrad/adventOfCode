import more_itertools

from days import parser
from days.utilities import timer


class Polymerisation:
    def __init__(self, template, rules):
        self.first_char = template[0][0]
        self.last_char = template[-1][-1]
        self.rules = rules
        self.single_chars = {x for x in self.rules.values()}
        self.state = {x: 0 for x in self.rules}
        for pair in template:
            self.state[pair] += 1

    def iteration(self):
        new_state = {x:0 for x in self.rules}
        for key, val in self.state.items():
            new_char = self.rules[key]
            new_state[key[0] + new_char] += val
            new_state[new_char + key[1]] += val
        self.state = new_state

    def iterate(self, n):
        for _ in range(n):
            self.iteration()

    def length(self):
        return sum(self.state.values()) + 1

    def get_occurences(self):
        occ = {x: 0 for x in self.single_chars}
        for k, v in self.state.items():
            occ[k[0]] += v
            occ[k[1]] += v
        occ[self.first_char] += 1
        occ[self.last_char] += 1
        occ = {k: v //2 for k, v in occ.items()}
        return occ


@timer
def part01(template, rules):
    pol = Polymerisation(template, rules)
    pol.iterate(10)
    occurences = pol.get_occurences()
    counts = [x for x in occurences.values()]
    return max(counts) - min(counts)


@timer
def part02(template, rules):
    pol = Polymerisation(template, rules)
    pol.iterate(40)
    occurences = pol.get_occurences()
    counts = [x for x in occurences.values()]
    return max(counts) - min(counts)


@timer
def load_data():
    d1, d2 = parser.load_two_things("day14.txt",
                                    lambda line: line.strip().split(),
                                    "\n",
                                    lambda line: line.strip().replace(" ", "").split("->"))
    d1 = d1[0][0]
    d1 = [d1[i] + d1[i+1] for i in range(len(d1)-1)]
    d2 = {x[0]: x[1] for x in d2}
    return d1, d2



@timer
def main():
    template, rules = load_data()
    print(template, rules)
    print(part01(template, rules))
    print(part02(template, rules))


if __name__ == "__main__":
    main()
