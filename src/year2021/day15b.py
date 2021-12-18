#!/usr/bin/env python3

import heapq
import itertools
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


class MinPriorityQueue:
    # Based on recipe from "Priority Queue Implementation Notes" at:
    # https://docs.python.org/3/library/heapq.html

    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = "<removed>"
        self.counter = itertools.count()

    def upsert(self, value: T.Hashable, priority: int) -> None:
        "Add a new value or update the priority of an existing value."
        if value in self.entry_finder:
            self.remove(value)
        count = next(self.counter)
        entry = [priority, count, value]
        self.entry_finder[value] = entry
        heapq.heappush(self.pq, entry)

    def remove(self, value: T.Hashable) -> None:
        "Mark an existing value as REMOVED. Raise KeyError if not found."
        entry = self.entry_finder.pop(value)
        entry[-1] = self.REMOVED

    def pop(self) -> T.Hashable:
        "Remove and return the lowest priority value. Raise KeyError if empty."
        while self.pq:
            priority, count, value = heapq.heappop(self.pq)
            if value is not self.REMOVED:
                del self.entry_finder[value]
                return value
        raise KeyError("Pop from an empty priority queue.")

    def contains(self, value: T.Hashable) -> bool:
        return value in self.entry_finder

    def empty(self) -> bool:
        return len(self.pq) == 0


def dijkstra(
    graph: dict[V2, int], source: V2, target: V2
) -> list[V2] | tuple[dict[V2, int], dict[V2, int]]:

    Q = MinPriorityQueue()
    dist = {}
    prev = {}

    dist[source] = 0
    for v in graph:
        if v != source:
            dist[v] = math.inf
            prev[v] = None
        Q.upsert(v, dist[v])

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
                Q.upsert(v, alt)

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
    with open("inputs/year2021/015.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
