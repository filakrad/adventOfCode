from days import parser
from days import utilities


class Board:
    def __init__(self, data):
        self.max_x = 0
        self.max_y = 0
        self.valid_points = dict()
        self.get_valid_points(data)

    def get_valid_points(self, data):
        for point1, point2 in data:
            if not self.are_points_valid(point1, point2):
                continue
            x_length = point2[0] - point1[0]
            y_length = point2[1] - point1[1]
            x_step = x_length//abs(x_length) if x_length != 0 else 0
            y_step = y_length//abs(y_length) if y_length != 0 else 0
            for i in range(0,max(abs(x_length + x_step), abs(y_length + y_step))):
                new_point = (point1[0] + i*x_step, point1[1] + i*y_step)
                utilities.add_to_dict(self.valid_points, new_point, 1)
                self.max_x = max(self.max_x, point1[0], point2[0])
                self.max_y = max(self.max_y, point1[1], point2[1])

    def are_points_valid(self, point1, point2):
        return point1[0] == point2[0] or point1[1] == point2[1]

    def result(self):
        return sum([v >= 2 for v in self.valid_points.values()])

    def __str__(self):
        out = ""
        for j in range(self.max_y + 1):
            for i in range(self.max_x + 1):
                if (i, j) in self.valid_points:
                    out += str(self.valid_points[(i, j)])
                else:
                    out += "."
            out += "\n"
        return out


class Board2(Board):
    def are_points_valid(self, point1, point2):
        return super().are_points_valid(point1, point2) or abs(point2[0] - point1[0]) == abs(point2[1] - point1[1])


if __name__ == "__main__":
    data = [[(9, 7),(7, 7)]]
    data = parser.load_rows_to_list("day05.txt", parser.parse_two_times, delim1="->", delim2=",", func=int)
    board = Board(data)
    # print(board)
    print(board.result())

    board = Board2(data)
    # print(board)
    print(board.result())
