from days import parser


class BingoGame:
    def __init__(self, sequence, cards):
        self.sequence = sequence
        self.cards = [BingoCard(card) for card in cards]

    def play(self):
        for new_number in self.sequence:
            for card in self.cards:
                if card.play_round(new_number):
                    print(new_number)
                    print(card)
                    return card.get_score(new_number)


class BingoCard:
    size = 5
    wins = [[i + j * 5 for i in range(5)] for j in range(5)]  # rows
    wins += [[5 * i + j for i in range(5)] for j in range(5)]  # columns
    # wins += [[6*i for i in range(5)], [4 + 4*i for i in range(5)]]  # diagonals

    def __init__(self, numbers):
        self.numbers = numbers
        self.hits = [False for _ in self.numbers]

    def play_round(self, new_number):
        new_index = self.numbers.index(new_number) if new_number in self.numbers else None
        if new_index is not None:
            self.hits[new_index] = True
            return self.is_win()
        return False

    def is_win(self):
        return any([all([self.hits[i] for i in win]) for win in self.wins])

    def get_score(self, new_number):
        unmarked = sum([x for i, x in enumerate(self.numbers) if not self.hits[i]])
        print(unmarked)
        return unmarked * new_number

    def __str__(self):
        out_str = ""
        for i in range(self.size):
            out_str += "".join("{:>3}".format(self.numbers[i*self.size + j]) for j in range(self.size)) \
                       + "   " + \
                       "".join("{:>3}".format("X" if self.hits[i*self.size + j] else "O") for j in range(self.size))\
                       + "\n"
        return out_str


class BingoGame2(BingoGame):
    def play(self):
        i = 0
        while self.cards:
            new_number = self.sequence[i]
            tmp_cards = self.cards.copy()
            for card in tmp_cards:
                if card.play_round(new_number):
                    last_card = card
                    self.cards.remove(card)
            i += 1
        return last_card.get_score(new_number)

if __name__ == "__main__":
    # header, cards = parser.load_bingo_cards("test.txt")
    header, cards = parser.load_bingo_cards("day04.txt")
    game = BingoGame(header, cards)
    print(game.play())

    game = BingoGame2(header, cards)
    print(game.play())