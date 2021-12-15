#!/usr/bin/env python3

import functools
import operator
import os
import re


BOUNDARY = 9


def parse_input(content: str) -> dict[tuple[int, int], int]:
    grid = {}
    rows = [
        list(map(int, re.findall(r"(\d)", line)))
        for line in filter(None, map(str.strip, content.split(os.linesep)))
    ]
    for y, row in enumerate(rows):
        for x, col in enumerate(row):
            grid[(x, y)] = col
    return grid


def neighbor_candidates(x: int, y: int) -> list[tuple[int, int]]:
    return [
        (x - 1, y),
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
    ]


def is_low_point(grid: dict[tuple[int, int], int], x: int, y: int) -> bool:
    for neighbor in neighbor_candidates(x, y):
        if neighbor not in grid:
            continue
        if grid[neighbor] <= grid[(x, y)]:
            return False
    return True


def flood_basin(
    grid: dict[tuple[int, int], int], boundary: int, x: int, y: int
) -> set[tuple[int, int]]:
    unvisited = set([(x, y)])
    visited = set()
    group = set()
    while unvisited:
        node = unvisited.pop()
        visited.add(node)
        if grid[node] < boundary:
            group.add(node)
        for neighbor in neighbor_candidates(*node):
            if neighbor not in grid:
                continue
            if neighbor in visited:
                continue
            if grid[neighbor] == boundary:
                continue
            unvisited.add(neighbor)
    return group


def solve(data: dict[tuple[int, int], int]) -> int:
    poi = {}
    for x, y in data:
        if is_low_point(data, x, y):
            poi[(x, y)] = data[(x, y)]

    basins = {(x, y): len(flood_basin(data, BOUNDARY, x, y)) for x, y in poi}
    return functools.reduce(operator.mul, sorted(basins.values())[-3:])


def main(runner=False):
    with open("inputs/009.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
