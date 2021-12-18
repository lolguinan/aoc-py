#!/usr/bin/env python3

import os
import re


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


def neighbor_candidates(x: int, y: int) -> list[list[int, int]]:
    return [
        [x - 1, y],
        [x, y - 1],
        [x + 1, y],
        [x, y + 1],
    ]


def is_low_point(grid: dict[tuple[int, int], int], x: int, y: int) -> bool:
    for nx, ny in neighbor_candidates(x, y):
        if (nx, ny) not in grid:
            continue
        if grid[(nx, ny)] <= grid[(x, y)]:
            return False
    return True


def solve(data: dict[tuple[int, int], int]) -> int:
    poi = {}
    for x, y in data:
        if is_low_point(data, x, y):
            poi[(x, y)] = data[(x, y)]
    return sum(value + 1 for value in poi.values())


def main(runner=False):
    with open("inputs/year2021/009.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
