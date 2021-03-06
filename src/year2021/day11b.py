#!/usr/bin/env python3

import math
import os

import colorama


def parse_input(content: str) -> list[list[int]]:
    return [
        list(map(int, list(row)))
        for row in filter(None, map(str.strip, content.split(os.linesep)))
    ]


def render_grid(grid: list[list[int]], colors=True) -> str:
    output = []
    for row in grid:
        output.append([])
        for col in row:
            prefix = None
            if col == 0:
                prefix = colorama.Style.BRIGHT
            else:
                prefix = colorama.Style.DIM
            if colors:
                output[-1].extend(
                    [
                        prefix,
                        str(col),
                        colorama.Style.NORMAL,
                    ]
                )
            else:
                output[-1].append(str(col))

    return os.linesep.join(["".join(row) for row in output])


def neighbor_candidates(x, y):
    return [
        (x - 1, y),
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
        (x, y + 1),
        (x - 1, y + 1),
    ]


def within(low, high, candidate):
    return candidate >= low and candidate <= high


def process_step(grid: list[list[int]]) -> list[list[int]]:
    height = len(grid)
    width = len(grid[0])

    output = [[grid[y][x] + 1 for x in range(width)] for y in range(height)]

    who_flashed = set()
    has_flashed = True
    while has_flashed:
        has_flashed = False
        for y in range(height):
            for x in range(width):
                if output[y][x] <= 9:
                    continue
                if (x, y) in who_flashed:
                    continue
                who_flashed.add((x, y))
                has_flashed = True
                for nx, ny in neighbor_candidates(x, y):
                    if not within(0, width - 1, nx):
                        continue
                    if not within(0, height - 1, ny):
                        continue
                    output[ny][nx] += 1

    for x, y in who_flashed:
        output[y][x] = 0

    return output


def solve(data: list[list[int]], steps: int) -> int:
    state = data
    step = 0
    while step < steps:
        step += 1
        state = process_step(state)
        synched = all([all([col == 0 for col in row]) for row in state])
        if synched:
            return step


def main(runner=False):
    with open("inputs/year2021/011.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data, math.inf)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
