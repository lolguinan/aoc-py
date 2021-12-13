#!/usr/bin/env python3

import collections
import math
import os
import re


ParsedInput = tuple[list[tuple[int, int]], list[tuple[str, int]]]
Grid = collections.Counter[tuple[int, int], int]


def parse_input(content: str) -> ParsedInput:
    dots = [
        tuple(map(int, match)) for match in re.findall(r"(\d+)\s*,\s*(\d+)", content)
    ]
    folds = [
        [direction, int(value)]
        for direction, value in re.findall(r"fold\s*along\s*([xy])\s*=(\d+)", content)
    ]
    return dots, folds


def render_grid(grid: Grid) -> str:
    min_x = min(x for x, y in grid)
    max_x = max(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_y = max(y for x, y in grid)

    rows = []
    for y in range(min_y, max_y + 1):
        rows.append([])
        for x in range(min_x, max_x + 1):
            if grid.get((x, y), None) is None:
                rows[-1].append(".")
            else:
                rows[-1].append("#")

    return os.linesep.join("".join(row) for row in rows)


def make_fold(grid: Grid, fold_instruction: tuple[str, int]) -> Grid:
    fold_along, fold_at = fold_instruction

    folded_grid = collections.Counter()
    for x, y in grid:
        dx, dy = x, y
        if fold_along == "x" and x > fold_at:
            dx = fold_at - (x - fold_at)
        elif fold_along == "y" and y > fold_at:
            dy = fold_at - (y - fold_at)
        folded_grid.update([(dx, dy)])
        if (x, y) != (dx, dy):
            folded_grid.subtract([(x, y)])
            if folded_grid[(x, y)] <= 0:
                del folded_grid[(x, y)]

    return folded_grid


def solve(data: ParsedInput, max_folds=math.inf) -> int:
    dots, folds = data
    grid = collections.Counter(dots)
    for index, fold in enumerate(folds):
        if index >= max_folds:
            break
        grid = make_fold(grid, fold)
    return len(grid)


def main(runner=False):
    with open("inputs/013.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data, 1)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
