#!/usr/bin/env python3

from __future__ import annotations
import dataclasses
import enum
import os
import re


@dataclasses.dataclass(frozen=True, order=True)
class Vector3:
    x: int
    y: int
    z: int


@dataclasses.dataclass(frozen=True, order=True)
class Cuboid:
    lower: Vector3
    upper: Vector3

    def volume(self):
        a = abs(self.upper.x - self.lower.x) + 1
        b = abs(self.upper.y - self.lower.y) + 1
        c = abs(self.upper.z - self.lower.z) + 1
        return a * b * c


class Toggle(enum.Enum):
    OFF = -1
    ON = 1

    def invert(self) -> Toggle:
        match self:
            case Toggle.ON:
                return Toggle.OFF
            case Toggle.OFF:
                return Toggle.ON


@dataclasses.dataclass
class RebootStep:
    toggle: Toggle
    cuboid: Cuboid


def parse_input(content: str) -> list[RebootStep]:
    pattern = r"^(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
    steps = []
    for row in filter(None, map(str.strip, content.split(os.linesep))):
        match = re.search(pattern, row)
        toggle = match.groups()[0]
        args = list(map(int, match.groups()[1:]))
        min_x = min(args[0], args[1])
        max_x = max(args[0], args[1])
        min_y = min(args[2], args[3])
        max_y = max(args[2], args[3])
        min_z = min(args[4], args[5])
        max_z = max(args[4], args[5])
        steps.append(
            RebootStep(
                Toggle.ON if toggle == "on" else Toggle.OFF,
                Cuboid(
                    Vector3(min_x, min_y, min_z),
                    Vector3(max_x, max_y, max_z),
                ),
            )
        )
    return steps


def does_intersect(a: Cuboid, b: Cuboid) -> bool:
    # https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_collision_detection
    return (
        True
        and (a.lower.x <= b.upper.x and a.upper.x >= b.lower.x)
        and (a.lower.y <= b.upper.y and a.upper.y >= b.lower.y)
        and (a.lower.z <= b.upper.z and a.upper.z >= b.lower.z)
    )


def one_d_overlap(
    a_lower: int, a_upper: int, b_lower: int, b_upper: int
) -> tuple[int, int]:
    # low a between b
    if b_lower <= a_lower <= b_upper:
        return a_lower, min(a_upper, b_upper)
    # low b between a
    elif a_lower <= b_lower <= a_upper:
        return b_lower, min(a_upper, b_upper)
    # high a between b
    elif b_lower <= a_upper <= b_upper:
        return max(a_lower, b_lower), a_upper
    # high b between a
    elif a_lower <= b_upper <= a_upper:
        return max(a_lower, b_lower), b_upper
    failure = f"a({a_lower},{a_upper}) and b({b_lower},{b_upper})"
    raise Exception("No overlap between {failure}")


def get_intersection(a: Cuboid, b: Cuboid) -> Cuboid | None:
    if not does_intersect(a, b):
        return None

    x0, x1 = one_d_overlap(a.lower.x, a.upper.x, b.lower.x, b.upper.x)
    y0, y1 = one_d_overlap(a.lower.y, a.upper.y, b.lower.y, b.upper.y)
    z0, z1 = one_d_overlap(a.lower.z, a.upper.z, b.lower.z, b.upper.z)

    return Cuboid(lower=Vector3(x0, y0, z0), upper=Vector3(x1, y1, z1))


def solve(steps: list[RebootStep]) -> int:
    cuboids: list[tuple[Cuboid, Toggle]] = []
    for step in steps:
        intersections: list[tuple[Cuboid, Toggle]] = []
        for cuboid, toggle in cuboids:
            # Invert the previous state of the intersected region. If it was ON
            # before, avoid double counting by marking this intersected region
            # OFF. If it was OFF before, the current ON step is re-enabling the
            # intersected region.
            if intersection := get_intersection(step.cuboid, cuboid):
                intersections.append((intersection, toggle.invert()))

        cuboids.extend(intersections)

        # Always store the ON cuboids. OFF cuboids are only represented
        # by their intersections with other ON cuboids.
        # NOTE: Adding this at the top of the loop and checking that
        # step.cuboid != cuboid in the inner loop above caused 3x run duration.
        # Lots of <string>.__eq__ from the generated dataclass __hash__ method.
        if step.toggle == Toggle.ON:
            cuboids.append((step.cuboid, step.toggle))

    return sum(cuboid.volume() * toggle.value for cuboid, toggle in cuboids)


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
