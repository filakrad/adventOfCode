from days import parser
from days.utilities import timer


length_types = {0: 15,
                1: 11}


def packet_factory(data):
    version, data = int(data[:3], 2), data[3:]
    type_id, data = int(data[:3], 2), data[3:]
    packets = []
    if type_id == 4:
        packets.append(LiteralPacket(version, type_id, data))
    else:
        packets.append(OperatorPacket(version, type_id, data))
    return packets


class LiteralPacket:
    def __init__(self, version, type_id, data):
        self.version = version
        self.type_id = type_id
        self.data = data
        self.value = self.get_value()

    def get_value(self):
        value = ''
        while self.data[0] == '1':
            part_val, self.data = self.data[1:5], self.data[5:]
            value += part_val
        part_val, self.data = self.data[1:5], self.data[5:]
        value += part_val
        return value


class OperatorPacket:
    def __init__(self, version, type_id, data):
        self.version = version
        self.type_id = type_id
        self.length_type_id, data = int(data[:1], 2), data[1:]
        length = length_types[self.length_type_id]
        self.packet_length, data = int(data[:length], 2), data[length:]
        self.data = data[:self.packet_length]
        self.rest_data = data[self.packet_length:]

def parse_packet(data):
    version, data = int(data[:3], 2), data[3:]
    print("version", version)
    type_id, data = int(data[:3], 2), data[3:]
    # print(type_id, data)
    value = 0
    sum_version = version
    if type_id == 4:
        part_value, data = parse_literals(data)
        print(part_value, data)
    else:
        part_version, part_value, data = parse_operator(data)
        sum_version += part_version
    value += part_value
    return sum_version, value, data


def parse_literals(data):
    value = ''
    while data[0] == '1':
        part_val, data = data[1:5], data[5:]
        value += part_val
    part_val, data = data[1:5], data[5:]
    value += part_val
    return int(value, 2), data


def parse_operator(data):
    length_type_id, data = int(data[:1], 2), data[1:]
    length = length_types[length_type_id]
    print(length, data)
    packet_length, data = int(data[:length], 2), data[length:]
    print(packet_length, data)
    sub_data, rest_data = data[:packet_length], data[packet_length:]

    sum_version = 0
    value = 0
    version = 0
    while sub_data and int(sub_data, 2) != 0:
        print("subpacket", sub_data)
        version, part_value, sub_data = parse_packet(sub_data)
        value += part_value
    sum_version += version
    return sum_version, value, rest_data



@timer
def part01(data):
    # print(data)
    # p = Packet(data)
    # print(data)
    # print(p.data)
    version, value, _ = parse_packet(data)
    print(version)



@timer
def part02(data):
    pass


@timer
def load_data():
    str_data = parser.load_rows_to_list("test.txt", lambda line: line)[0]
    print(str_data)
    # int_data = [int(x, 16) for x in str_data]
    # print(int_data)
    bit_str = f'{int(str_data, 16):0>{len(str_data)*4}b}'
    return bit_str


@timer
def main():
    data = load_data()
    print(data)
    print(part01(data))
    print(part02(data))


if __name__ == "__main__":
    main()
