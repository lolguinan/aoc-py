#!/usr/bin/env python3

import math
import os

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


def dijkstra(
    graph: dict[V2, int], source: V2, target: V2
) -> list[V2] | tuple[dict[V2, int], dict[V2, int]]:
    def min_dist(Q, dist):
        u = None
        for v in Q:
            if u is None or dist[v] < dist[u]:
                u = v
        return u

    Q = set()
    dist = {}
    prev = {}

    for v in graph:
        dist[v] = math.inf
        prev[v] = None
        Q.add(v)
    dist[source] = 0

    while Q:
        u = min_dist(Q, dist)

        Q.remove(u)

        if u == target:
            S = []
            if prev[u] is not None or u == source:
                while u is not None:
                    S.insert(0, u)
                    u = prev[u]
            return S

        for v in get_neighbors(u):
            if v not in Q:
                continue
            alt = dist[u] + graph[v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

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


def solve(data: dict[V2, int]) -> int:
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
