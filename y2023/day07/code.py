from enum import Enum

from y2023.utilities import timer


class Type(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OA_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

    def __lt__(self, other):
        return self.value < other.value


card_dict = {str(i): i for i in range(2, 10)}
card_dict.update({'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14})

card_dict_2 = {str(i): i for i in range(2, 10)}
card_dict_2.update({'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14})


class Hand:
    def __init__(self, line):
        x = line.split(' ')
        self.bid = int(x[1])
        self.cards = self.fill_cards(x)
        self.type = self.get_type()

    @staticmethod
    def fill_cards(x):
        return [card_dict[c] for c in x[0]]

    def get_type(self):
        set_ = set(self.cards)
        counts = [self.cards.count(x) for x in set_]
        counts.sort()
        set_size = len(set_)
        if set_size == 1:
            return Type.FIVE_OF_A_KIND
        elif counts[-1] == 4:
            return Type.FOUR_OF_A_KIND
        elif set_size == 2:
            return Type.FULL_HOUSE
        elif counts[-1] == 3:
            return Type.THREE_OA_A_KIND
        elif set_size == 3:
            return Type.TWO_PAIR
        elif set_size == 4:
            return Type.ONE_PAIR
        else:
            return Type.HIGH_CARD

    def __lt__(self, other):
        if self.type != other.type:
            return self.type < other.type
        for i in range(5):
            if self.cards[i] != other.cards[i]:
                return self.cards[i] < other.cards[i]

    def __str__(self):
        return f"{self.cards} {self.type} {self.bid}"


class Hand02(Hand):
    def __init__(self, line):
        super().__init__(line)

    @staticmethod
    def fill_cards(x):
        return [card_dict_2[c] for c in x[0]]

    def get_type(self):
        if 1 not in self.cards:
            return super().get_type()
        jokers = self.cards.count(1)
        no_joker = [c for c in self.cards if c != 1]

        set_ = set(no_joker)
        counts = [no_joker.count(x) for x in set_]
        counts.sort()
        set_size = len(set_)

        if set_size <= 1:
            return Type.FIVE_OF_A_KIND
        elif counts[-1] + jokers == 4:
            return Type.FOUR_OF_A_KIND
        elif set_size == 2:
            return Type.FULL_HOUSE
        elif counts[-1] + jokers == 3:
            return Type.THREE_OA_A_KIND
        else:
            return Type.ONE_PAIR

@timer
def parse(file_name, part=1):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    if part == 1:
        return [Hand(l) for l in lines]
    else:
        return [Hand02(l) for l in lines]


@timer
def part01(data):
    winnings = 0
    sorted_data = sorted(data)
    for i, h in enumerate(sorted_data):
        winnings += (i+1) * h.bid
    return winnings

@timer
def part02(data):
    winnings = 0
    sorted_data = sorted(data)
    for i, h in enumerate(sorted_data):
        winnings += (i+1) * h.bid
    return winnings


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    data = parse("data.txt", part=2)
    print(part02(data))