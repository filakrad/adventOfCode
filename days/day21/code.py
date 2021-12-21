import queue
from itertools import product

from days import parser
from days.utilities import timer, add_to_dict


class DeterministicDie:
    def __init__(self, n):
        self.max_value = n
        self.values = list(range(1, n + 1))
        self.rolls = 0

    def roll(self):
        self.rolls += 1
        return self.values[(self.rolls - 1) % self.max_value]


class Player:
    def __init__(self, starting_position):
        self.position = starting_position
        self.score = 0
        self.win = False


class Game:
    def __init__(self, die, players, win_value):
        self.die = die
        self.players = players
        self.win_value = win_value
        self.max_plan_value = 10
        self.game_plan = [i for i in range(1, self.max_plan_value+1)]

    def play(self):
        i = 0
        while True:
            player = self.players[i % 2]
            rolls = sum([self.die.roll() for _ in range(3)])
            player.position = self.game_plan[(player.position - 1 + rolls) % self.max_plan_value]
            player.score += player.position
            if player.score >= self.win_value:
                player.win = True
                break
            i += 1

    def get_score(self):
        player = [p for p in self.players if p.win][0]
        return player.score * self.die.rolls


class DiracDie:
    values = [sum(x) for x in product(range(1, 3 + 1), range(1, 3 + 1), range(1, 3 + 1))]
    val_dict = {}
    for v in values:
        add_to_dict(val_dict, v, 1)
    sorted_values = sorted(list(set(values)))
    max_pos = len(sorted_values) - 1

    def __init__(self, n):
        self.current_val_dict = {}
        for v in self.sorted_values:
            self.current_val_dict[v] = self.val_dict[v] * n
        self.current_pos = 0


class Game2(Game):
    def play(self):
        dice = [DiracDie(1)]
        for p in self.players:
            p.score = []
            p.position = [p.position]
            p.wins = 0
        i = 0
        while dice:
            player = self.players[i % 2]
            rolls = dice[-1].sorted_values[dice[-1].current_pos]
            pos = self.game_plan[(player.position[-1] - 1 + rolls) % self.max_plan_value]
            player.score.append(pos)
            player.position.append(pos)
            if sum(player.score) >= self.win_value:
                player.wins += dice[-1].current_val_dict[rolls]
                player.score.pop()
                player.position.pop()
                dice[-1].current_pos += 1
                while dice[-1].current_pos > dice[-1].max_pos:
                    dice.pop()
                    if not dice:
                        break
                    dice[-1].current_pos += 1

                    i -= 1
                    self.players[i % 2].score.pop()
                    self.players[i % 2].position.pop()
            else:
                dice.append(DiracDie(dice[-1].current_val_dict[rolls]))
                i += 1

    def get_score(self):
        return max([p.wins for p in self.players])


@timer
def part01(data):
    die = DeterministicDie(100)
    players = [Player(d) for d in data]
    game = Game(die, players, 1000)
    game.play()
    return game.get_score()


@timer
def part02(data):
    players = [Player(d) for d in data]
    game = Game2(None, players, 21)
    game.play()
    return game.get_score()


@timer
def load_data():
    return parser.load_rows_to_list("day21.txt", lambda line: int(line.strip().split(" ")[-1]))



@timer
def main():
    data = load_data()
    print(data)
    print(part01(data))
    print(part02(data))


if __name__ == "__main__":
    main()
