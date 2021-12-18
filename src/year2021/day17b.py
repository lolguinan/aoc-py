#!/usr/bin/env python3

import dataclasses
import os
import re


@dataclasses.dataclass(frozen=True)
class Vector2:
    x: int
    y: int


@dataclasses.dataclass(frozen=True)
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


def render(b: Target, steps: list[Vector2]) -> str:
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


def launch_probe(target: Target, velocity: Vector2) -> bool:
    position = Vector2(0, 0)
    while True:
        position, velocity = step_position(position, velocity)
        if within_area(target, position):
            return True
        if overshot(target, position):
            return False


def all_initial_velocity_hits(target: Target) -> set[Vector2]:
    velocities = set()

    for x in range(target.upper.x + 1):
        for y in range(-abs(target.lower.y), abs(target.lower.y) + 1):
            v = Vector2(x, y)
            if launch_probe(target, v):
                velocities.add(v)

    return velocities


def solve(data: Target) -> int:
    return len(all_initial_velocity_hits(data))


def main(runner=False):
    with open("inputs/year2021/017.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
