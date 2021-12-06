from days.parser import load_rows_to_list


sample_data = [199,
            200,
            208,
            210,
            200,
            207,
            240,
            269,
            260,
            263]

def get_increases(data):
    bools = [x - y < 0 for x, y in zip(data, data[1:])]
    return sum(bools)


def get_sliding_increases(data):
    sums = [sum(t) for t in zip(data, data[1:], data[2:])]
    return get_increases(sums)

if __name__ == "__main__":
    data = load_rows_to_list("data01.txt", int)
    # data = sample_data
    print(get_increases(data))
    print(get_sliding_increases(data))