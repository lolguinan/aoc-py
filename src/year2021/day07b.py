#!/usr/bin/env python3

import collections
import functools
import os


def parse_input(content: str) -> list[int]:
    for row in content.split(os.linesep):
        if not row.strip():
            continue
        return list(map(int, filter(None, map(str.strip, row.split(",")))))


def get_step_count(start: int, stop: int) -> int:
    return abs(start - stop)


@functools.cache
def get_move_cost(steps: int) -> int:
    return sum(range(steps + 1))


def get_costs(positions: list[int]) -> dict[int, int]:
    costs = {}
    groups = collections.Counter(positions)
    for candidate in range(min(positions), max(positions) + 1):
        costs[candidate] = 0
        for pos, count in groups.items():
            move_cost = get_move_cost(get_step_count(pos, candidate))
            costs[candidate] += move_cost * count
    return costs


def solve(positions: list[int]) -> tuple[int, int]:
    costs = get_costs(positions)
    for k, v in sorted(costs.items(), key=lambda kv: kv[1]):
        return v


def main(runner=False):
    with open("inputs/007.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
