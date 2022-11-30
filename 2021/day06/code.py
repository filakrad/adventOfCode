from days.utilities import add_to_dict
from days import parser


class Ocean:
    def __init__(self, fish_list):
        self.reset_number = 6
        self.new_fish_number = 8
        self.fish_dict = dict()
        for fish in fish_list:
            add_to_dict(self.fish_dict, fish, 1)

    def simulate(self, num_days):
        for _ in range(num_days):
            tmp_dict = dict()
            for f in self.fish_dict:
                if f-1 < 0:
                    add_to_dict(tmp_dict, self.reset_number, self.fish_dict[f])
                    add_to_dict(tmp_dict, self.new_fish_number, self.fish_dict[f])
                else:
                    add_to_dict(tmp_dict, f-1, self.fish_dict[f])
            self.fish_dict = tmp_dict

    def result(self):
        return sum(self.fish_dict.values())


if __name__ == "__main__":
    init = [3,4,3,1,2]
    init = parser.load_rows_to_list("day06.txt", lambda x: [int(i) for i in x.split(",")])[0]
    ocean = Ocean(init)
    ocean.simulate(80)
    print(ocean.result())

    ocean = Ocean(init)
    ocean.simulate(256)
    print(ocean.result())