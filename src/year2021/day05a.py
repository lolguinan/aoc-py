#!/usr/bin/env python3

import re
import os


def parse_input(content: str) -> list[list[int]]:
    return [
        # x1, y1, x2, y2
        list(map(int, re.findall(r"(\d+)", line)))
        for line in filter(None, map(str.strip, content.split(os.linesep)))
    ]


def render_grid(grid: dict) -> str:
    min_x = min(x for x, y in grid)
    max_x = max(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_y = max(y for x, y in grid)

    table = []
    for y in range(min_y, max_y + 1):
        table.append([])
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                table[-1].append(str(len(grid[(x, y)])))
            else:
                table[-1].append(".")

    return os.linesep.join(["".join(row) for row in table])


def apply_points(
    line_segments: list[list[int]],
) -> dict[tuple[int, int], list[list[int]]]:
    grid = {}
    for line_segment in line_segments:
        x1, y1, x2, y2 = line_segment
        # only consider horizontal and vertical lines
        if not (x1 == x2 or y1 == y2):
            continue
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid.setdefault((x1, y), []).append(line_segment)
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid.setdefault((x, y1), []).append(line_segment)
    return grid


def solve(line_segments: list[list[int]]) -> int:
    grid = apply_points(line_segments)
    return sum([1 if len(values) >= 2 else 0 for values in grid.values()])


def main():
    with open("inputs/005.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    print(answer)


if __name__ == "__main__":
    main()
