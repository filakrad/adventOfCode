from days import parser
from days.utilities import timer


def get_graph(data):
    vertices = list(set.union(*[set(x) for x in data]))
    graph = {x: set() for x in vertices}
    for edge in data:
        graph[edge[0]].add(edge[1])
        graph[edge[1]].add(edge[0])
    return graph


def get_all_paths(graph, current_node, current_path=None, all_paths=None):
    if current_path is None:
        current_path = []
        all_paths = []

    current_path.append(current_node)
    if current_node == 'end':
        all_paths.append(tuple(current_path))
        return

    for next in graph[current_node]:
        if next in current_path and str.islower(next[0]):
            continue
        get_all_paths(graph, next, [x for x in current_path], all_paths)

    return all_paths


def get_all_paths_02(graph, current_node, twice, current_path=None, all_paths=None):
    if current_path is None:
        current_path = []
        all_paths = []

    current_path.append(current_node)
    if current_node == 'end':
        all_paths.append(tuple(current_path))
        return

    twice_num = twice[1]

    for next in graph[current_node]:
        if next in current_path and str.islower(next[0]):
            if next == twice[0] and twice_num < 2:
                pass
            else:
                continue
        get_all_paths_02(graph, next, (twice[0], twice_num+1 if next == twice[0] else twice_num), [x for x in current_path], all_paths)

    return all_paths


@timer
def part01(data):
    graph = get_graph(data)
    all_paths = get_all_paths(graph, "start")
    return len(all_paths)


@timer
def part02(data):
    graph = get_graph(data)
    total_paths = set()
    all_lower = [x for x in graph if str.islower(x[0])]
    all_lower.remove('start')
    all_lower.remove('end')

    for low in all_lower:
        part_paths = get_all_paths_02(graph, "start", (low, 0))
        total_paths = total_paths.union(set(part_paths))
    return len(total_paths)


@timer
def load_data():
    return parser.load_rows_to_list("day12.txt", lambda x: x.strip().split("-"))


@timer
def main():
    data = load_data()
    print(part01(data))
    print(part02(data))


if __name__ == "__main__":
    main()