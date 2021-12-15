from days import parser
from days.utilities import timer

from queue import PriorityQueue
import copy

class Graph:
    neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def __init__(self, data):
        self.max_x = len(data[0])
        self.max_y = len(data)
        self.vertices = [(i, j) for j in range(self.max_y) for i in range(self.max_x)]
        self.num_vertices = self.max_x * self.max_y
        self.edges = self.get_edges(data)

    def get_edges(self, data):
        edges = {(i, j): [] for j in range(self.max_y) for i in range(self.max_x)}
        for e in edges:
            for n in self.neighbors:
                cx = e[0] + n[0]
                cy = e[1] + n[1]
                if 0 <= cx < self.max_x and 0 <= cy < self.max_y:
                    edges[e].append(((cx, cy), data[cy][cx]))
        return edges


def dijkstra(graph, start_vertex):
    D = {v:float('inf') for v in graph.vertices}
    D[start_vertex] = 0

    visited = set()

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        visited.add(current_vertex)
        neighbors = graph.edges[current_vertex]

        for neighbor in neighbors:
            distance = neighbor[1]
            if neighbor[0] not in visited:
                old_cost = D[neighbor[0]]
                new_cost = D[current_vertex] + distance
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor[0]))
                    D[neighbor[0]] = new_cost

    return D


def upscale_data(data):
    part_upscaled = []
    for d_row in data:
        part_upscaled.append([((d+i-1) % 9) + 1 for i in range(5) for d in d_row])
    upscaled = []
    for i in range(5):
        for d_row in part_upscaled:
            upscaled.append([((d + i - 1) % 9) + 1 for d in d_row])
    return upscaled


@timer
def part01(data):
    graph = Graph(data)
    lengths = dijkstra(graph, (0, 0))
    return lengths[(graph.max_x - 1, graph.max_y - 1)]


@timer
def part02(data):
    new_data = upscale_data(data)
    graph = Graph(new_data)
    lengths = dijkstra(graph, (0, 0))
    return lengths[(graph.max_x - 1, graph.max_y - 1)]


@timer
def load_data():
    return parser.load_rows_to_list("day15.txt", lambda line: [int(x) for x in line.strip()])


@timer
def main():
    data = load_data()
    print(data)
    print(part01(data))
    print(part02(data))


if __name__ == "__main__":
    main()