#!/usr/bin/env python3

import collections
import enum
import os


OPEN = "([{<"
CLOSE = ")]}>"


SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


class Status(enum.Enum):
    LEGAL = 0
    INCOMPLETE = 1
    CORRUPTED = 2


ParseResult = collections.namedtuple(
    "ParseResult",
    [
        "status",
        "illegal_index",
        "expected",
        "actual",
    ],
)


def parse_input(content: str) -> list[list[str]]:
    return list(filter(None, map(str.strip, content.split(os.linesep))))


def is_pair(lhs: str, rhs: str) -> bool:
    return OPEN.index(lhs) == CLOSE.index(rhs)


def parse(chunks: str) -> ParseResult:
    if len(chunks) % 2 != 0:
        ParseResult(Status.INCOMPLETE, None, None, None)
    stack = []
    for index, token in enumerate(chunks):
        if token in OPEN:
            stack.append(token)
        elif token in CLOSE:
            prev = stack.pop()
            if not is_pair(prev, token):
                expected = CLOSE[OPEN.index(prev)]
                return ParseResult(Status.CORRUPTED, index, expected, token)
        else:
            raise Exception(f"Unknown token: {token}")
    return ParseResult(Status.LEGAL, None, None, None)


def solve(data: list[list[str]]) -> int:
    score = 0
    for line in data:
        result = parse(line)
        if result.status != Status.CORRUPTED:
            continue
        score += SCORE[result.actual]
    return score


def main():
    with open("inputs/010.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    print(answer)


if __name__ == "__main__":
    main()
