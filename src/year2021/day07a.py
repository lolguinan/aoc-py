#!/usr/bin/env python3

import collections
import os


def parse_input(content: str) -> list[int]:
    for row in content.split(os.linesep):
        if not row.strip():
            continue
        return list(map(int, filter(None, map(str.strip, row.split(",")))))


def get_costs(positions: list[int]) -> dict[int, int]:
    costs = {}
    groups = collections.Counter(positions)
    for candidate in range(min(positions), max(positions) + 1):
        costs[candidate] = 0
        for pos, count in groups.items():
            costs[candidate] += abs(pos - candidate) * count
    return costs


def solve(positions: list[int]) -> tuple[int, int]:
    costs = get_costs(positions)
    for k, v in sorted(costs.items(), key=lambda kv: kv[1]):
        return v


def main(runner=False):
    with open("inputs/year2021/007.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
