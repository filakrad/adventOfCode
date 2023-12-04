from y2023.utilities import timer


@timer
def parse(file_name):
    with open(file_name, "r") as f:
        cards = dict()
        for line in f.readlines():
            card, rest = line.strip().split(":")
            wins, haves = rest.split("|")
            card_id = int(card.split(" ")[-1])
            win_nums = [int(x) for x in wins.split(" ") if x]
            have_nums = [int(x) for x in haves.split(" ") if x]
            cards[card_id] = {"win": win_nums, "have": have_nums}
    return cards


@timer
def part01(data):
    total = 0
    for i, card in data.items():
        nums = set(card["win"]).intersection(set(card["have"]))
        if len(nums):
            total += 2**(len(nums)-1)
    return total


@timer
def part02(data):
    cards = {i: 1 for i in data.keys()}
    for i, card in data.items():
        nums = set(card["win"]).intersection(set(card["have"]))
        for j in range(1, len(nums)+1):
            cards[i+j] += cards[i]
    return sum(cards.values())


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    print(part02(data))