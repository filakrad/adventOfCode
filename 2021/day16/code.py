from days import parser
from days.utilities import timer

from queue import Queue
import math


class LiteralPacket:
    def __init__(self, version, type_id, data):
        self.version = version
        self.type_id = type_id
        self.data = data
        self.value = self.get_value()

    def get_value(self):
        value = ''
        is_last = get_n_int(1, self.data) == 0
        while not is_last:
            part_val = get_n_str(4, self.data)
            value += part_val
            is_last = get_n_int(1, self.data) == 0
        part_val = get_n_str(4, self.data)
        value += part_val
        return int(value, 2)


class OperatorPacket:
    def __init__(self, version, type_id, data):
        self.version = version
        self.type_id = type_id
        self.length_type_id = get_n_int(1, data)
        self.data = data
        self.subpackets = []
        if self.length_type_id == 0:
            self.resolve_length_id_0()
        else:
            self.resolve_length_id_1()

    def resolve_length_id_0(self):
        length = get_n_int(15, self.data)
        sub_data_str = get_n_str(length, self.data)
        sub_data = Queue()
        for b in sub_data_str:
            sub_data.put(b)
        while sub_data.qsize() > 0:
            sub_packet = parse_packet(sub_data)
            self.subpackets.append(sub_packet)

    def resolve_length_id_1(self):
        sub_packets_num = get_n_int(11, self.data)
        for _ in range(sub_packets_num):
            sub_packet = parse_packet(self.data)
            self.subpackets.append(sub_packet)


def parse_packet(data):
    version = get_n_int(3, data)
    type_id = get_n_int(3, data)
    if type_id == 4:
        packet = LiteralPacket(version, type_id, data)
    else:
        packet = OperatorPacket(version, type_id, data)
    return packet


def get_n_int(n, data):
    new_str = ''
    for _ in range(n):
        new_str += data.get()
    return int(new_str, 2)


def get_n_str(n, data):
    new_str = ''
    for _ in range(n):
        new_str += data.get()
    return new_str


def get_version_sum(packet):
    version = packet.version
    if isinstance(packet, LiteralPacket):
        return packet.version
    for p in packet.subpackets:
        version += get_version_sum(p)
    return version


def value_decoder(packet):
    if isinstance(packet, LiteralPacket):
        return packet.value
    sub_values = [value_decoder(p) for p in packet.subpackets]
    if packet.type_id == 0:
        return sum(sub_values)
    elif packet.type_id == 1:
        return math.prod(sub_values)
    elif packet.type_id == 2:
        return min(sub_values)
    elif packet.type_id == 3:
        return max(sub_values)
    elif packet.type_id == 5:
        return int(sub_values[0] > sub_values[1])
    elif packet.type_id == 6:
        return int(sub_values[0] < sub_values[1])
    elif packet.type_id == 7:
        return int(sub_values[0] == sub_values[1])


@timer
def part01(data):
    packet = parse_packet(data)
    return get_version_sum(packet)


@timer
def part02(data):
    packet = parse_packet(data)
    return value_decoder(packet)


@timer
def load_data():
    str_data = parser.load_rows_to_list("day16.txt", lambda line: line)[0]
    bit_str = f'{int(str_data, 16):0>{len(str_data)*4}b}'
    bit_queue = Queue()
    for b in bit_str:
        bit_queue.put(b)
    return bit_queue


@timer
def main():
    data = load_data()
    print(part01(data))
    data = load_data()
    print(part02(data))


if __name__ == "__main__":
    main()
