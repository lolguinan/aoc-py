#!/usr/bin/env python3

import collections
import os
import re


def parse_input(content: str) -> list[int]:
    for row in content.split(os.linesep):
        if not row.strip():
            continue
        return list(map(int, filter(None, map(str.strip, row.split(",")))))


def step_day(state: dict[int, int]) -> dict[int, int]:
    sim = {}

    for fish in state:
        if fish == 0:
            sim[6] = sim.get(6, 0) + state[fish]
            sim[8] = sim.get(8, 0) + state[fish]
        else:
            sim[fish - 1] = sim.get(fish - 1, 0) + state[fish]

    return sim


def solve(initial_state: list[int], days: int) -> int:
    current_state = collections.Counter(initial_state)
    for day in range(days):
        current_state = step_day(current_state)

    return sum(current_state.values())


def main():
    with open("inputs/006.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data, 256)
    print(answer)


if __name__ == "__main__":
    main()
