#!/usr/bin/env python3

import pytest

import year2021.day12a as day


def test_example_10_paths():
    case = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""
    data = day.parse_input(case)
    expected = set(
        [
            ("start", "A", "b", "A", "c", "A", "end"),
            ("start", "A", "b", "A", "end"),
            ("start", "A", "b", "end"),
            ("start", "A", "c", "A", "b", "A", "end"),
            ("start", "A", "c", "A", "b", "end"),
            ("start", "A", "c", "A", "end"),
            ("start", "A", "end"),
            ("start", "b", "A", "c", "A", "end"),
            ("start", "b", "A", "end"),
            ("start", "b", "end"),
        ]
    )
    actual = set(map(tuple, day.dfs(data, "start")))
    assert expected == actual


def test_example_19_paths():
    case = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""
    data = day.parse_input(case)
    expected = set(
        [
            ("start", "HN", "dc", "HN", "end"),
            ("start", "HN", "dc", "HN", "kj", "HN", "end"),
            ("start", "HN", "dc", "end"),
            ("start", "HN", "dc", "kj", "HN", "end"),
            ("start", "HN", "end"),
            ("start", "HN", "kj", "HN", "dc", "HN", "end"),
            ("start", "HN", "kj", "HN", "dc", "end"),
            ("start", "HN", "kj", "HN", "end"),
            ("start", "HN", "kj", "dc", "HN", "end"),
            ("start", "HN", "kj", "dc", "end"),
            ("start", "dc", "HN", "end"),
            ("start", "dc", "HN", "kj", "HN", "end"),
            ("start", "dc", "end"),
            ("start", "dc", "kj", "HN", "end"),
            ("start", "kj", "HN", "dc", "HN", "end"),
            ("start", "kj", "HN", "dc", "end"),
            ("start", "kj", "HN", "end"),
            ("start", "kj", "dc", "HN", "end"),
            ("start", "kj", "dc", "end"),
        ]
    )
    actual = set(map(tuple, day.dfs(data, "start")))
    assert expected == actual


def test_example_226_paths():
    case = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""
    data = day.parse_input(case)
    expected = 226
    actual = day.solve(data)
    assert expected == actual
