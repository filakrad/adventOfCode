from days import parser


class Submarine:
    def __init__(self, x, y):
        self.horizontal = x
        self.depth = y

    def forward(self, x):
        self.horizontal += x

    def up(self, y):
        self.depth -= y

    def down(self, y):
        self.up(-y)

    def do_string_instruction(self, instruction, *args):
        getattr(self, instruction)(*args)

    def do_instructions(self, data):
        for d in data:
            self.do_string_instruction(*d)


class Submarine2(Submarine):
    def __init__(self, x, y, aim):
        super().__init__(x, y)
        self.aim = aim

    def forward(self, x):
        self.horizontal += x
        self.depth += self.aim * x

    def up(self, y):
        self.aim -= y


sample_instructions = [("forward", 5),
                        ("down", 5),
                        ("forward", 8),
                        ("up", 3),
                        ("down", 8),
                        ("forward", 2)]

if __name__ == "__main__":
    # instructions = sample_instructions
    instructions = parser.load_rows_to_list("day02.txt", parser.delimited_values, delimiter=" ", functions=[str, int])
    sub = Submarine(0, 0)
    sub.do_instructions(instructions)
    print(sub.depth * sub.horizontal)

    sub = Submarine2(0, 0, 0)
    sub.do_instructions(instructions)
    print(sub.depth * sub.horizontal)