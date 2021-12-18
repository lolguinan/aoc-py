#!/usr/bin/env python3

import os


OPEN = "([{<"
CLOSE = ")]}>"


SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def parse_input(content: str) -> list[list[str]]:
    return list(filter(None, map(str.strip, content.split(os.linesep))))


def is_pair(lhs: str, rhs: str) -> bool:
    return OPEN.index(lhs) == CLOSE.index(rhs)


def parse_incomplete(chunks: str) -> list[str]:
    stack = []
    for index, token in enumerate(chunks):
        if token in OPEN:
            stack.append(token)
        elif token in CLOSE:
            prev = stack.pop()
            if not is_pair(prev, token):
                return None
        else:
            raise Exception(f"Unknown token: {token}")
    return [CLOSE[OPEN.index(token)] for token in reversed(stack)]


def get_score(chunks: str) -> int:
    score = 0
    for token in chunks:
        score = (score * 5) + SCORE[token]
    return score


def solve(data: list[list[str]]) -> int:
    scores = []
    for line in data:
        result = parse_incomplete(line)
        if not result:
            continue
        scores.append(get_score("".join(result)))
    return sorted(scores)[len(scores) // 2]


def main(runner=False):
    with open("inputs/year2021/010.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
