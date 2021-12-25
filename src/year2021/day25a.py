#!/usr/bin/env python3

import dataclasses
import enum
import os


class Mobile(str, enum.Enum):
    EAST = ">"
    SOUTH = "v"


@dataclasses.dataclass(frozen=True)
class Vector2:
    x: int
    y: int


@dataclasses.dataclass
class State:
    grid: dict[Vector2, Mobile]
    width: int
    height: int


def parse_input(content: str) -> State:
    grid = {}

    rows = list(filter(None, map(str.strip, content.split(os.linesep))))
    height = len(rows)
    width = len(rows[0])

    for y, row in enumerate(rows):
        for x, col in enumerate(row):
            try:
                grid[Vector2(x, y)] = Mobile(col)
            except ValueError:
                pass

    return State(grid, width, height)


def render_grid(state: State):
    output = []
    for y in range(state.height):
        output.append([])
        for x in range(state.width):
            output[-1].append(state.grid.get(Vector2(x, y), "."))

    return os.linesep.join("".join(row) for row in output)


def movement_target(
    width: int, height: int, mobile: Mobile, position: Vector2
) -> Vector2:
    match mobile:
        case Mobile.EAST:
            return Vector2((position.x + 1) % width, position.y)
        case Mobile.SOUTH:
            return Vector2(position.x, (position.y + 1) % height)
        case _:
            raise Exception(f'Unknown mobile: {mobile}')


def step_move(state: State, mobile_type: Mobile = None) -> State:
    if mobile_type is None:
        for mobile_type in Mobile:
            state = step_move(state, mobile_type)
        return state

    sim = {}

    for v in state.grid:
        mobile = state.grid[v]
        if mobile != mobile_type:
            sim[v] = mobile
            continue
        v1 = movement_target(state.width, state.height, mobile, v)
        if v1 in state.grid:
            sim[v] = mobile
            continue
        sim[v1] = mobile

    return State(sim, state.width, state.height)


def solve(data: State) -> int:
    prev = curr = data
    counter = 0
    while True:
        counter += 1
        curr = step_move(curr)
        if prev == curr:
            break
        prev = curr
    return counter


def main(runner=False):
    with open("inputs/year2021/025.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
