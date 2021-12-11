from collections import deque
from statistics import median

from days import parser
from days.utilities import timer


syntax_score = {")": 3,
                "]": 57,
                "}": 1197,
                ">": 25137}

autocomplete_score = {")": 1,
                      "]": 2,
                      "}": 3,
                      ">": 4}


class Validation:
    right_to_left = {"}": "{", ">": "<", ")": "(", "]": "["}
    left_values = [x for x in right_to_left.values()]

    def __init__(self, chunks):
        self.input = chunks
        self.validation_stack = deque()

    def get_invalid(self):
        for brace in self.input:
            if brace in self.left_values:
                self.validation_stack.append(brace)
            else:
                if len(self.validation_stack) == 0:
                    return brace
                last = self.validation_stack.pop()
                if self.right_to_left[brace] != last:
                    return brace
        return None


class AutoComplete(Validation):
    left_to_right = {y: x for x, y in Validation.right_to_left.items()}

    def get_closures(self):
        if self.get_invalid() is not None:
            return None
        closures = []
        while self.validation_stack:
            closures.append(self.left_to_right[self.validation_stack.pop()])
        return closures


@timer
def part01(data):
    total_score = 0
    for row in data:
        validation = Validation(row)
        if (brace := validation.get_invalid()) is not None:
            total_score += syntax_score[brace]
    return total_score


@timer
def part02(data):
    all_scores = []
    for row in data:
        autocomplete = AutoComplete(row)
        if (closures := autocomplete.get_closures()) is not None:
            local_score = 0
            for brace in closures:
                local_score = local_score * 5 + autocomplete_score[brace]
            all_scores.append(local_score)
    return median(all_scores)


@timer
def load_data():
    return parser.load_rows_to_list("day10.txt", lambda x: [i for i in x.strip()])


@timer
def main():
    data = load_data()
    print(part01(data))
    print(part02(data))


if __name__ == "__main__":
    main()