#!/usr/bin/env python3

import dataclasses
import math
import os
import re


@dataclasses.dataclass
class Vector2:
    x: int
    y: int


@dataclasses.dataclass
class Bounds:
    lower: Vector2
    upper: Vector2


def parse_input(content: str) -> Bounds:
    match = re.findall(r"([-]?\d+)", content)
    x0, x1, y0, y1 = map(int, match)
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    return Bounds(Vector2(x0, y0), Vector2(x1, y1))


def within_area(b: Bounds, p: Vector2) -> bool:
    return b.lower.x <= p.x <= b.upper.x and b.lower.y <= p.y <= b.upper.y


def overshot(b: Bounds, p: Vector2) -> bool:
    return p.x > b.upper.x or p.y < b.lower.y


def step_position(p: Vector2, v: Vector2) -> tuple[Vector2, Vector2]:
    p2 = Vector2(p.x + v.x, p.y + v.y)
    v2 = Vector2(v.x - 1 if v.x > 0 else v.x + 1 if v.x < 0 else v.x, v.y - 1)
    return p2, v2


def render(b: Bounds, steps: list[Vector2]) -> str:
    poi = {}
    for bx in range(b.lower.x, b.upper.x + 1):
        for by in range(b.lower.y, b.upper.y + 1):
            poi[(bx, by)] = "T"
    origin = Vector2(0, 0)
    for step in steps:
        poi[dataclasses.astuple(step)] = "S" if step == origin else "#"

    min_x = min(x for x, y in poi)
    max_x = max(x for x, y in poi)
    min_y = min(y for x, y in poi)
    max_y = max(y for x, y in poi)

    grid = []
    for y in range(min_y, max_y + 1):
        grid.append([])
        for x in range(min_x, max_x + 1):
            grid[-1].append(poi.get((x, y), "."))

    return os.linesep.join("".join(row) for row in reversed(grid))


def launch_probe(bounds: tuple[Vector2, Vector2], velocity: Vector2):
    position = Vector2(0, 0)
    steps = [position]
    while True:
        position, velocity = step_position(position, velocity)
        steps.append(position)
        if within_area(bounds, position):
            return True, steps
        if overshot(bounds, position):
            return False, steps


def nat_sum_to(n):
    return (n * (n + 1)) / 2


def solve(data: Bounds) -> int:
    try_up_to = 1_000

    x_candidates = []
    for x in range(try_up_to + 1):
        nat_sum = nat_sum_to(x)
        if nat_sum < data.lower.x:
            continue
        if nat_sum > data.upper.x:
            break
        x_candidates.append(x)

    try_up_to = abs(data.lower.y)

    max_y = -math.inf
    for x in x_candidates:
        for y in range(-try_up_to, try_up_to + 1):
            hit, steps = launch_probe(data, Vector2(x, y))
            if hit:
                max_y = max(max_y, max(step.y for step in steps))

    return max_y


def main(runner=False):
    with open("inputs/017.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
