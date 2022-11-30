from days import parser


def get_minimal_fuel_01(positions):
    fuels = [sum([abs(p - i) for p in positions]) for i in range(max(positions))]
    return min(fuels)


def get_minimal_fuel_02(positions):
    fuels = [sum([((abs(p - i)) * (abs(p - i) + 1) // 2) for p in positions]) for i in range(max(positions))]
    return min(fuels)


if __name__ == "__main__":
    positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    positions = parser.load_rows_to_list("day07.txt", lambda x: [int(i) for i in x.split(",")])[0]

    print(get_minimal_fuel_01(positions))

    print(get_minimal_fuel_02(positions))