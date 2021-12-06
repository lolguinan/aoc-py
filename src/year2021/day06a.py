#!/usr/bin/env python3

import re
import os


def parse_input(content: str) -> list[int]:
    for row in content.split(os.linesep):
        if not row.strip():
            continue
        return list(map(int, filter(None, map(str.strip, row.split(",")))))


def step_day(state: list[int]) -> None:
    i = 0
    initial_size = len(state)
    while i < initial_size:
        fish = state[i]
        if fish == 0:
            state[i] = 6
            state.append(8)
        else:
            state[i] -= 1
        i += 1


def solve(initial_state: list[int], days: int) -> int:
    current_state = list(initial_state)
    for day in range(days):
        step_day(current_state)

    return len(current_state)


def main():
    with open("inputs/006.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data, 80)
    print(answer)


if __name__ == "__main__":
    main()
