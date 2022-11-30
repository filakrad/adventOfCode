from days import parser


sample_data = ["00100",
                "11110",
                "10110",
                "10111",
                "10101",
                "01111",
                "00111",
                "11100",
                "10000",
                "11001",
                "00010",
                "01010"]

def get_zeros_number(data):
    total_zeros = [0 for _ in data[0]]
    for row in data:
        for i, bit in enumerate(row):
            total_zeros[i] += bit == "0"
    return total_zeros


def task_01(data):
    total_zeros = get_zeros_number(data)
    total_length = len(data)
    half_total_length = total_length/2
    print(total_zeros)
    total_ones = [total_length - zero for zero in total_zeros]
    print(total_ones)
    gamma = "".join(["0" if zero > half_total_length else "1" for zero in total_zeros])
    print(gamma)
    epsilon = "".join(["1" if zero == "0" else "0" for zero in gamma])
    print(epsilon)
    return int(gamma, 2) * int(epsilon, 2)


def get_zeros_number_on_index(data, index):
    return sum([x[index] == "0" for x in data])


def task_02(data):
    tmp = data

    idx = 0
    while len(tmp) > 1:
        total_zeros = get_zeros_number_on_index(tmp, idx)
        half_total_length = len(tmp) / 2
        if total_zeros - half_total_length > 0:
            new_data = filter(lambda x: x[idx] == "0", tmp)
        else:
            new_data = filter(lambda x: x[idx] == "1", tmp)
        tmp = list(new_data)
        idx += 1
    oxygen = int(tmp[0], 2)
    print(tmp, oxygen)

    tmp = data
    idx = 0
    while len(tmp) > 1:
        total_zeros = get_zeros_number_on_index(tmp, idx)
        half_total_length = len(tmp) / 2
        if total_zeros - half_total_length <= 0:
            new_data = filter(lambda x: x[idx] == "0", tmp)
        else:
            new_data = filter(lambda x: x[idx] == "1", tmp)
        tmp = list(new_data)
        idx += 1
    co2 = int(tmp[0], 2)
    print(tmp, co2)
    return oxygen * co2

if __name__ == "__main__":
    data = parser.load_rows_to_list("day03.txt", parser.string_without_newline)
    # print(data)
    # data = sample_data
    print(task_01(data))
    print(task_02(data))