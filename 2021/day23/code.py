import functools

from days.utilities import timer


TYPES = ["A", "B", "C", "D"]
MOUTHS = [2+2*i for i in range(4)]
SCORES = [1, 10, 100, 1000]


class Amphipod:
    def __init__(self, atype, room, position):
        self.type = TYPES.index(atype)
        self.room = room
        self.position = position

    def is_movable(self, rooms, hallway):
        if self.is_home(rooms):
            return False
        if self.room is None:
            target = rooms[self.type]
            if not target.is_accepting:
                return False
            return all([x is None for x in hallway[min(self.position+1, target.mouth):max(self.position, target.mouth)]])
        this_room = rooms[self.room]
        if any([x is not None for x in this_room.positions[:self.position]]):
            return False
        return any(x is None for x in [hallway[this_room.mouth - 1], hallway[this_room.mouth + 1]])

    def get_targets(self, rooms, hallway):
        if self.room is None:
            return [(self.type, sum([x is None for x in rooms[self.type].positions]) - 1)]
        minim = 0
        maxim = len(hallway)
        for i, a in enumerate(hallway):
            if a is not None:
                if i < rooms[self.room].mouth:
                    minim = max(i + 1, minim)
                else:
                    maxim = min(i, maxim)
        return [(None, i) for i in range(minim, maxim) if i not in MOUTHS]

    def move(self, target, rooms, hallway):
        if self.room is None:
            hallway[self.position] = None
            rooms[target[0]].positions[target[1]] = self
            rooms[target[0]].check_accepting()
        else:
            rooms[self.room].positions[self.position] = None
            rooms[self.room].check_accepting()
            hallway[target[1]] = self
        self.room = target[0]
        self.position = target[1]

    def is_home(self, rooms):
        return self.type == self.room and rooms[self.type].is_accepting

    def __str__(self):
        return f"{TYPES[self.type]}, {self.room}, {self.position}"


class Room:
    def __init__(self, rtype, data):
        self.type = rtype
        self.positions = [Amphipod(a, self.type, i) for i, a in enumerate(data)]
        self.mouth = 2+2*self.type
        self.is_accepting = False

    def check_accepting(self):
        self.is_accepting = all([x.type == self.type for x in self.positions if x is not None])

    def is_full(self):
        return all([self.type == p.type if p is not None else False for p in self.positions])


class Burrow:
    def __init__(self, data):
        self.hallway = [None for _ in range(11)]
        self.rooms = [Room(i, data[i]) for i in range(4)]
        self.all_pods = [x for room in self.rooms for x in room.positions]

    def is_finished(self):
        return all([r.is_full() for r in self.rooms])

    def __str__(self):
        out = "".join("#" for _ in range(len(self.hallway) + 2)) + "\n"
        out += "#" + "".join([TYPES[a.type] if a is not None else "." for a in self.hallway]) + "#\n"
        for i in range(len(self.rooms[0].positions)):
            pad = "###" if i == 0 else "  #"
            out += f"{pad}" + "#".join([TYPES[room.positions[i].type] if room.positions[i] is not None else "." for room in self.rooms]) + f"{pad[::-1]}\n"
        out += "  #########  "
        return out

@functools.lru_cache(maxsize=500)
def get_score(positions, pod_type):
    hall = list(filter(lambda x: x[0] is None, positions))[0]
    room = list(filter(lambda x: x[0] is not None, positions))[0]
    length = abs(hall[1] - MOUTHS[room[0]]) + room[1] + 1
    return length * SCORES[pod_type]


def random_walk(burrow, moves=None, current_score=None, max_score=None):

    if burrow.is_finished():
        tmp = max_score[0]
        max_score[0] = min(max_score[0], sum(x[2] for x in moves))
        if tmp != max_score[0]:
            print(moves)
            print(max_score[0])
        return

    movables = []
    for pod in burrow.all_pods:
        if pod.is_movable(burrow.rooms, burrow.hallway):
            movables.append(pod)

    if step_to_tuple(burrow) == test_tuple:
        print([str(x) for x in movables])
        for pod in movables:
            targets = pod.get_targets(burrow.rooms, burrow.hallway)
            print(pod, targets)

    for pod in movables:
        current_pos = (pod.room, pod.position)
        targets = pod.get_targets(burrow.rooms, burrow.hallway)
        # print(pod, targets)
        for target in targets:
            score = get_score((current_pos, target), pod.type)
            if current_score[0] + score < max_score[0]:
                current_score[0] += score
                pod.move(target, burrow.rooms, burrow.hallway)
                moves.append((current_pos, target, score))
                random_walk(burrow, moves, current_score, max_score)
                del moves[-1]
                current_score[0] -= score
                pod.move(current_pos, burrow.rooms, burrow.hallway)
    # return False


def step_to_tuple(burrow):
    hall = [x.type if x is not None else -1 for x in burrow.hallway]
    rooms = [x.type if x is not None else -1 for room in burrow.rooms for x in room.positions]
    return tuple(hall + rooms)


str_to_int = {".": -1,
              "A": 0,
              "B": 1,
              "C": 2,
              "D": 3}


def get_test_tuple():
    strng = """#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########"""
    splitted = strng.split("\n")
    hall = [ str_to_int[x] for x in splitted[1] if x in str_to_int ]
    rows = [[str_to_int[x] for x in row if x in str_to_int] for row in splitted[2:-1]]
    rooms = [rows[j][i] for i in range(4) for j in range(4)]
    return tuple(hall + rooms)

test_tuple = get_test_tuple()
print(test_tuple)


def test(burrow):
    burrow.rooms[0].positions[0].move((None, 5), burrow.rooms, burrow.hallway)
    burrow.rooms[1].positions[0].move((None, 10), burrow.rooms, burrow.hallway)
    burrow.rooms[1].positions[1].move((None, 9), burrow.rooms, burrow.hallway)
    burrow.rooms[1].positions[2].move((None, 3), burrow.rooms, burrow.hallway)
    burrow.rooms[1].positions[3].move((None, 0), burrow.rooms, burrow.hallway)
    burrow.hallway[5].move((1, 3), burrow.rooms, burrow.hallway)
    burrow.rooms[1].positions[3].move((None, 9), burrow.rooms, burrow.hallway)
    burrow.hallway[3].move((1, 3), burrow.rooms, burrow.hallway)
    burrow.rooms[1].positions[3].move((None, 1), burrow.rooms, burrow.hallway)


    print(burrow)

    movables = []
    for pod in burrow.all_pods:
        if pod.is_movable(burrow.rooms, burrow.hallway):
            movables.append(pod)
    for pod in movables:
        targets = pod.get_targets(burrow.rooms, burrow.hallway)
        print(pod, targets)


@timer
def part01(data):
    data = [["B", "C"], ["C", "D"], ["A", "D"], ["B", "A"]]
    burrow = Burrow(data)
    way = []
    current_score = [0]
    max_score = [1000000]
    random_walk(burrow, way, current_score, max_score)
    return max_score[0]


@timer
def part02(data):
    data = [["B", "D", "D", "C"], ["C", "C", "B", "D"], ["A", "B", "A", "D"], ["B", "A", "C", "A"]]
    # data = [["B", "D", "D", "A"], ["C", "C", "B", "D"], ["B", "B", "A", "C"], ["D", "A", "C", "A"]]
    burrow = Burrow(data)
    way = []
    current_score = [0]
    max_score = [10000000000]
    random_walk(burrow, way, current_score, max_score)
    return max_score[0]


@timer
def load_data():
    pass


@timer
def main():
    data = load_data()
    # print(part01(data))
    print(part02(data))


if __name__ == "__main__":
    main()