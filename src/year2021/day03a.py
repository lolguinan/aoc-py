#!/usr/bin/env python3

import collections
import os


def parse_input(content: str) -> list[list[int]]:
    return [
        list(map(int, list(row)))
        for row in filter(None, map(str.strip,
            content.split(os.linesep)))
    ]


def solve(data: list[list[int]]) -> int:
    gamma_rate = []
    epsilon_rate = []

    for index in range(len(data[0])):
        counts = collections.Counter([
            row[index] for row in data
        ])
        (most, _), (least, _) = counts.most_common()
        gamma_rate.append(most)
        epsilon_rate.append(least)

    gamma_rate = int(''.join(map(str, gamma_rate)), 2)
    epsilon_rate = int(''.join(map(str, epsilon_rate)), 2)

    power_consumption = gamma_rate * epsilon_rate

    return power_consumption


def main():
    with open('inputs/003.txt') as fp:
        content = fp.read()

    data = parse_input(content)
    power_consumption = solve(data)
    print(power_consumption)


if __name__ == '__main__':
    main()
