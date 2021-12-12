#!/usr/bin/env python3

import os
import string
import typing as T

import colorama


def parse_input(content: str) -> dict[str, list[str]]:
    result = {}
    for row in filter(None, map(str.strip, content.split(os.linesep))):
        lhs, rhs = filter(None, map(str.strip, row.split("-")))
        if lhs == "end":
            lhs, rhs = rhs, lhs
        result.setdefault(lhs, []).append(rhs)
        if rhs != "end":
            result.setdefault(rhs, []).append(lhs)
    return result


def is_big(s: str) -> bool:
    return all(ch in string.ascii_uppercase for ch in s)


def dfs(
    graph: dict[str, list[str]],
    node: str,
    visited: set[str] = None,
    ancestors: list[str] = None,
) -> T.Iterator[list[str]]:
    if visited is None:
        visited = set()
    visited.add(node)
    if ancestors is None:
        ancestors = []

    if node == "end":
        yield ancestors + [node]

    visited.add(node)
    for child in graph.get(node, []):
        if child not in visited or is_big(child):
            yield from dfs(graph, child, visited.copy(), ancestors + [node])


def solve(graph: dict[str, list[str]]) -> int:
    paths = 0
    for path in dfs(graph, "start"):
        paths += 1
    return paths


def main(runner=False):
    with open("inputs/012.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
