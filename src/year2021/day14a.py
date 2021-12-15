#!/usr/bin/env python3

from __future__ import annotations
import collections
import re
import typing as T


Rules = dict[tuple[str, str], str]
ParsedInput = tuple[str, Rules]


def parse_input(content: str) -> ParsedInput:
    template = re.findall(r"^\s*([A-Z]+)\s*$", content, flags=re.MULTILINE)

    rules = re.findall(
        r"\s*".join(["^", "([A-Z]{2})", "-", ">", "([A-Z]{1})", "$"]),
        content,
        flags=re.MULTILINE,
    )

    template = template[0]
    rules = {tuple(pair): elem for pair, elem in rules}

    return template, rules


class Node:
    def __init__(self, value=None, left: Node = None, right: Node = None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self) -> str:
        s = []
        current = self
        while current is not None:
            s.append(current.value)
            current = current.right
        return "".join(s)

    @staticmethod
    def build(src: T.Iterable) -> Node:
        root = current = None

        for elem in src:
            if root is None:
                root = Node(value=elem)
                current = root
                continue
            current.right = Node(value=elem, left=current)
            current = current.right

        return root


def apply_rules(link_root: Node, rules: Rules) -> Node:
    current = link_root
    while current.right is not None:
        pair = (current.value, current.right.value)
        if pair not in rules:
            continue
        right = current.right
        current.right = Node(rules[pair], current, right)
        right.left = current.right

        current = current.right
        current = current.right

    return link_root


def solve(data: ParsedInput, max_steps: int) -> int:
    template, rules = data
    link_root = Node.build(template)

    for _ in range(max_steps):
        link_root = apply_rules(link_root, rules)

    counts = collections.Counter(str(link_root))
    counts = counts.most_common()
    _, most_common = counts[0]
    _, least_common = counts[-1]

    return most_common - least_common


def main(runner=False):
    with open("inputs/014.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data, 10)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
