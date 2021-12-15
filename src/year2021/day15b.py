#!/usr/bin/env python3

import math
import os
import typing as T

import colorama


V2 = tuple[int, int]


def parse_input(content: str) -> dict[V2, int]:
    rows = [
        list(map(int, list(row)))
        for row in filter(None, map(str.strip, content.split(os.linesep)))
    ]
    graph = {}
    for y, row in enumerate(rows):
        for x, col in enumerate(row):
            graph[(x, y)] = col
    return graph


def get_neighbors(xy: V2) -> list[V2]:
    x, y = xy
    return [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]


def get_corners(graph: dict[V2, int]) -> tuple[V2, V2]:
    min_x = min(x for x, y in graph)
    min_y = min(y for x, y in graph)
    max_x = max(x for x, y in graph)
    max_y = max(y for x, y in graph)

    return (min_x, min_y), (max_x, max_y)


class FakeMinPriorityQueue:
    def __init__(self):
        self.heap: dict[int, set[T.Hashable]] = {}

    def push(self, priority: int, value: T.Hashable):
        self.heap.setdefault(priority, set()).add(value)

    def replace(self, priority: int, value: T.Hashable):
        keys = self.find(value)
        if keys is not None:
            for key in keys:
                self.heap[key].remove(value)
        self.push(priority, value)

    def pop(self) -> T.Hashable:
        key = min(self.heap)
        values = self.heap[key]
        if len(values) > 1:
            return values.pop()
        del self.heap[key]
        return values.pop()

    def find(self, value) -> list[T.Hashable] | None:
        keys = []
        for key in self.heap:
            if value in self.heap[key]:
                keys.append(key)
        if keys:
            return keys
        return None

    def contains(self, value) -> bool:
        return self.find(value) is not None

    def empty(self) -> bool:
        return len(self.heap) == 0

    def sizes(self) -> dict[int, int]:
        return dict((key, len(self.heap[key])) for key in self.heap)


def dijkstra(
    graph: dict[V2, int], source: V2, target: V2
) -> list[V2] | tuple[dict[V2, int], dict[V2, int]]:

    Q = FakeMinPriorityQueue()
    dist = {}
    prev = {}

    dist[source] = 0
    for v in graph:
        if v != source:
            dist[v] = math.inf
            prev[v] = None
        Q.push(dist[v], v)

    while not Q.empty():
        u = Q.pop()

        if u == target:
            S = []
            if prev[u] is not None or u == source:
                while u is not None:
                    S.insert(0, u)
                    if u not in prev:
                        break
                    u = prev[u]
            return S

        for v in get_neighbors(u):
            if not Q.contains(v):
                continue
            alt = dist[u] + graph[v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                Q.replace(alt, v)

    return dist, prev


def render_dijkstra(graph: dict[V2, int], path: list[V2]) -> str:
    (min_x, min_y), (max_x, max_y) = get_corners(graph)

    output = []
    for y in range(min_y, max_y + 1):
        output.append([])
        for x in range(min_x, max_x + 1):
            output[-1].append(graph[(x, y)])
            if (x, y) in path:
                output[-1][-1] = "{}{}{}".format(
                    colorama.Style.BRIGHT,
                    output[-1][-1],
                    colorama.Style.RESET_ALL,
                )

    return os.linesep.join("".join(map(str, row)) for row in output)


def render_graph(graph: dict[V2, int]) -> str:
    (min_x, min_y), (max_x, max_y) = get_corners(graph)

    output = []
    for y in range(min_y, max_y + 1):
        output.append([])
        for x in range(min_x, max_x + 1):
            output[-1].append(graph.get((x, y), "."))

    return os.linesep.join("".join(map(str, row)) for row in output)


def expand_dimensions(graph: dict[V2, int], multiplier: int) -> dict[V2, int]:
    (min_x, min_y), (max_x, max_y) = get_corners(graph)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    expanded = graph.copy()

    # complete first row by expanding right
    for offset in range(1, multiplier):
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                ex = x + offset * width
                ey = y

                vx = x
                if offset > 0:
                    vx = x + (offset - 1) * width
                vy = y

                v = expanded[(vx, vy)] + 1
                if v > 9:
                    v = 1
                expanded[(ex, ey)] = v

    (min_x, min_y), (max_x, max_y) = get_corners(expanded)

    # complete remaining rows by expanding down
    for offset in range(1, multiplier):
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                ex = x
                ey = y + offset * width

                vx = x
                vy = y
                if offset > 0:
                    vy = y + (offset - 1) * width

                v = expanded[(vx, vy)] + 1
                if v > 9:
                    v = 1
                expanded[(ex, ey)] = v

    return expanded


def solve(data: dict[V2, int]) -> int:
    data = expand_dimensions(data, 5)
    (min_x, min_y), (max_x, max_y) = get_corners(data)

    path = dijkstra(data, (min_x, min_y), (max_x, max_y))

    return sum(data[xy] for xy in path[1:])


def main(runner=False):
    with open("inputs/015.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
