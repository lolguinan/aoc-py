#!/usr/bin/env python3

from __future__ import annotations
import enum
import functools
import itertools
import json
import math
import operator
import os
import re


class Pair:
    def __init__(
        self,
        parent: Pair = None,
        left: Pair = None,
        right: Pair = None,
        value: int = None,
    ):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value

    def walk(self):
        if self.left:
            yield from self.left.walk()
        yield self
        if self.right:
            yield from self.right.walk()

    def depth(self):
        count = 0
        node = self
        while node.parent:
            count += 1
            node = node.parent
        return count

    @staticmethod
    def build(expr: list | int, parent: Pair = None) -> Pair:
        pair = Pair(parent)
        left, right = expr
        if isinstance(left, list):
            pair.left = Pair.build(left, pair)
        elif isinstance(left, int):
            pair.left = Pair(parent=pair, value=left)
        else:
            raise Exception(f"Unknown left type: {type(left)}")
        if isinstance(right, list):
            pair.right = Pair.build(right, pair)
        elif isinstance(right, int):
            pair.right = Pair(parent=pair, value=right)
        else:
            raise Exception(f"Unknown right type: {type(right)}")
        return pair

    def clone(self, parent: Pair = None):
        p = Pair(parent=parent, value=self.value)
        if self.left:
            p.left = self.left.clone(p)
        if self.right:
            p.right = self.right.clone(p)
        return p

    def to_list(self):
        expr = []
        if self.value is None:
            expr.append(self.left.to_list())
            expr.append(self.right.to_list())
            return expr
        return self.value

    def to_dict(self):
        return {
            "parented": self.parent is not None,
            "left": self.left if not self.left else self.left.to_dict(),
            "right": self.right if not self.right else self.right.to_dict(),
            "value": self.value,
        }

    def __repr__(self):
        return str(self.to_list()).replace(" ", "")


def parse_input(content: str) -> list[Pair]:
    return [
        Pair.build(json.loads(row))
        for row in filter(None, map(str.strip, content.split(os.linesep)))
    ]


class Bias(enum.Enum):
    LEFT = 0
    RIGHT = 1


def find_leaf(source: Pair, bias: Bias) -> Pair | None:
    left = operator.attrgetter("left")
    right = operator.attrgetter("right")
    ascent = left if bias == Bias.LEFT else right
    descent = left if bias == Bias.RIGHT else right

    visited = [source]
    current = source.parent
    while current is not None and ascent(current) in visited:
        visited.append(current)
        current = current.parent
    if current is None:
        return None

    if ascent(current) is None:
        return current
    current = ascent(current)

    while current.value is None:
        current = descent(current)

    return current


def can_explode(pair: Pair) -> bool:
    return (
        pair.depth() == 4
        and pair.value is None
        and pair.left.value is not None
        and pair.right.value is not None
    )


def explode(pair: Pair) -> tuple[bool, Pair]:
    source = None
    for node in pair.walk():
        if can_explode(node):
            source = node
            break
    else:
        return False, pair

    left_node = find_leaf(source, Bias.LEFT)
    if left_node:
        left_node.value += source.left.value

    right_node = find_leaf(source, Bias.RIGHT)
    if right_node:
        right_node.value += source.right.value

    replacement = Pair(parent=source.parent, value=0)
    if source.parent.left == source:
        source.parent.left = replacement
    else:
        source.parent.right = replacement

    return True, pair


def can_split(pair: Pair) -> bool:
    return pair.value is not None and pair.value >= 10


def split(pair: Pair) -> tuple[bool, Pair]:
    source = None
    for node in pair.walk():
        if can_split(node):
            source = node
            break
    else:
        return False, pair

    replacement = Pair.build(
        [
            source.value // 2,
            int(math.ceil(source.value / 2)),
        ],
        source.parent,
    )
    if source.parent.left == source:
        source.parent.left = replacement
    else:
        source.parent.right = replacement

    return True, pair


def try_reduce(pair: Pair) -> Pair:
    while True:
        check, pair = explode(pair)
        if check:
            continue
        check, pair = split(pair)
        if check:
            continue
        break
    return pair


def add(left: Pair, right: Pair) -> Pair:
    parent = Pair(left=left, right=right)
    left.parent = parent
    right.parent = parent
    return try_reduce(parent)


def add_many(pairs: list[Pair]) -> Pair:
    return functools.reduce(add, pairs)


def magnitude(pair: Pair) -> int:
    if pair.value is not None:
        return pair.value
    return 3 * magnitude(pair.left) + 2 * magnitude(pair.right)


def solve(data: list[Pair]) -> int:
    magnitudes = {}
    for left, right in itertools.permutations(range(len(data)), 2):
        magnitudes[(left, right)] = magnitude(
            add_many(
                [
                    data[left].clone(),
                    data[right].clone(),
                ]
            )
        )
    return max(magnitudes.values())


def main(runner=False):
    with open("inputs/year2021/018.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
