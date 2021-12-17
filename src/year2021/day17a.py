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
class Target:
    lower: Vector2
    upper: Vector2


def parse_input(content: str) -> Target:
    match = re.findall(r"([-]?\d+)", content)
    x0, x1, y0, y1 = map(int, match)
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    return Target(Vector2(x0, y0), Vector2(x1, y1))


def render(t: Target, steps: list[Vector2]) -> str:
    poi = {}
    for tx in range(t.lower.x, t.upper.x + 1):
        for ty in range(t.lower.y, t.upper.y + 1):
            poi[(tx, ty)] = "T"
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


def within_area(t: Target, p: Vector2) -> bool:
    return t.lower.x <= p.x <= t.upper.x and t.lower.y <= p.y <= t.upper.y


def overshot(t: Target, p: Vector2) -> bool:
    return p.x > t.upper.x or p.y < t.lower.y


def step_position(p: Vector2, v: Vector2) -> tuple[Vector2, Vector2]:
    p2 = Vector2(p.x + v.x, p.y + v.y)
    v2 = Vector2(v.x - 1 if v.x > 0 else v.x + 1 if v.x < 0 else v.x, v.y - 1)
    return p2, v2


def launch_probe(target: Target, velocity: Vector2) -> tuple[bool, list[Vector2]]:
    position = Vector2(0, 0)
    steps = [position]
    while True:
        position, velocity = step_position(position, velocity)
        steps.append(position)
        if within_area(target, position):
            return True, steps
        if overshot(target, position):
            return False, steps


def solve(data: Target) -> int:
    max_y = -math.inf

    for x in range(data.upper.x + 1):
        for y in range(-abs(data.lower.y), abs(data.lower.y) + 1):
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
