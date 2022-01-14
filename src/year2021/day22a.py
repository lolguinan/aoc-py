#!/usr/bin/env python3

import dataclasses
import enum
import os
import re
import typing as T


class Toggle(enum.Enum):
    OFF = 0
    ON = 1


@dataclasses.dataclass(frozen=True)
class Vector3:
    x: int
    y: int
    z: int


@dataclasses.dataclass
class RebootStep:
    toggle: Toggle
    lower: Vector3
    upper: Vector3


def parse_input(content: str) -> list[RebootStep]:
    pattern = r"^(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
    steps = []
    for row in filter(None, map(str.strip, content.split(os.linesep))):
        match = re.search(pattern, row)
        toggle, args = match.groups()[0], list(map(int, match.groups()[1:]))
        min_x = min(args[0], args[1])
        max_x = max(args[0], args[1])
        min_y = min(args[2], args[3])
        max_y = max(args[2], args[3])
        min_z = min(args[4], args[5])
        max_z = max(args[4], args[5])
        steps.append(
            RebootStep(
                Toggle.ON if toggle == "on" else Toggle.OFF,
                Vector3(min_x, min_y, min_z),
                Vector3(max_x, max_y, max_z),
            )
        )
    return steps


def points_in_region(lower: Vector3, upper: Vector3) -> T.Iterator[Vector3]:
    lower_bound = Vector3(-50, -50, -50)
    upper_bound = Vector3(50, 50, 50)

    min_x = max(lower_bound.x, lower.x)
    min_y = max(lower_bound.y, lower.y)
    min_z = max(lower_bound.z, lower.z)

    max_x = min(upper_bound.x, upper.x)
    max_y = min(upper_bound.y, upper.y)
    max_z = min(upper_bound.z, upper.z)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                yield Vector3(x, y, z)


def in_bounds(point: Vector3, lower: Vector3, upper: Vector3) -> bool:
    return (
        lower.x <= point.x <= upper.x
        and lower.y <= point.y <= upper.y
        and lower.z <= point.z <= upper.z
    )


def solve(steps: list[RebootStep]) -> int:
    grid = {}
    for step in steps:
        for point in points_in_region(step.lower, step.upper):
            grid[point] = step.toggle

    return sum(1 if grid[point] == Toggle.ON else 0 for point in grid)


def main(runner=False):
    with open("inputs/year2021/022.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
