#!/usr/bin/env python3

import os


SEGMENTS = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}


def parse_input(content: str) -> list[tuple[list[str], list[str]]]:
    rows = list(filter(None, map(str.strip, content.split(os.linesep))))
    rows = [list(map(str.strip, row.split("|"))) for row in rows]
    rows = [
        (
            a.split(),
            b.split(),
        )
        for a, b in rows
    ]
    return rows


def solve(data: list[tuple[list[str], list[str]]]) -> int:
    unique_segment_lengths = [
        len(SEGMENTS[1]),
        len(SEGMENTS[4]),
        len(SEGMENTS[7]),
        len(SEGMENTS[8]),
    ]
    appearances = 0
    for patterns, output in data:
        for digit in output:
            if len(digit) in unique_segment_lengths:
                appearances += 1
    return appearances


def main(runner=False):
    with open("inputs/008.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
