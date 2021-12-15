#!/usr/bin/env python3

import collections
import functools
import os
import string
import typing as T

import colorama


def parse_input(content: str) -> dict[str, list[str]]:
    result = {}
    for row in filter(None, map(str.strip, content.split(os.linesep))):
        lhs, rhs = filter(None, map(str.strip, row.split("-")))

        # can't go to a start
        if rhs == "start":
            lhs, rhs = rhs, lhs
        # can't come from an end
        if lhs == "end":
            lhs, rhs = rhs, lhs
        # could still have a two-node graph of start-end though...

        result.setdefault(lhs, []).append(rhs)
        if len(set([rhs, lhs]) - set(["start", "end"])) == 2:
            result.setdefault(rhs, []).append(lhs)

    return result


@functools.cache
def is_big(s: str) -> bool:
    return all(ch in string.ascii_uppercase for ch in s)


@functools.cache
def is_small(s: str) -> bool:
    return all(ch in string.ascii_lowercase for ch in s)


def dfs(
    graph: dict[str, list[str]],
    node: str,
    visited: collections.Counter = None,
    ancestors: list[str] = None,
) -> T.Iterator[list[str]]:

    if visited is None:
        visited = collections.Counter()
    if ancestors is None:
        ancestors = []

    if node == "end":
        yield ancestors + [node]

    if node not in visited or is_small(node):
        visited[node] += 1

    has_small_twice = visited.total() > len(visited)

    for child in graph.get(node, []):
        if child == "end":
            yield ancestors + [node, child]
        elif is_big(child) or child not in visited or not has_small_twice:
            yield from dfs(
                graph, child, collections.Counter(visited), ancestors + [node]
            )


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
