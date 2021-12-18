#!/usr/bin/env python3

import pytest

import year2021.day12b as day


def test_example_36_paths():
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
            ("start", "A", "b", "A", "b", "A", "c", "A", "end"),
            ("start", "A", "b", "A", "b", "A", "end"),
            ("start", "A", "b", "A", "b", "end"),
            ("start", "A", "b", "A", "c", "A", "b", "A", "end"),
            ("start", "A", "b", "A", "c", "A", "b", "end"),
            ("start", "A", "b", "A", "c", "A", "c", "A", "end"),
            ("start", "A", "b", "A", "c", "A", "end"),
            ("start", "A", "b", "A", "end"),
            ("start", "A", "b", "d", "b", "A", "c", "A", "end"),
            ("start", "A", "b", "d", "b", "A", "end"),
            ("start", "A", "b", "d", "b", "end"),
            ("start", "A", "b", "end"),
            ("start", "A", "c", "A", "b", "A", "b", "A", "end"),
            ("start", "A", "c", "A", "b", "A", "b", "end"),
            ("start", "A", "c", "A", "b", "A", "c", "A", "end"),
            ("start", "A", "c", "A", "b", "A", "end"),
            ("start", "A", "c", "A", "b", "d", "b", "A", "end"),
            ("start", "A", "c", "A", "b", "d", "b", "end"),
            ("start", "A", "c", "A", "b", "end"),
            ("start", "A", "c", "A", "c", "A", "b", "A", "end"),
            ("start", "A", "c", "A", "c", "A", "b", "end"),
            ("start", "A", "c", "A", "c", "A", "end"),
            ("start", "A", "c", "A", "end"),
            ("start", "A", "end"),
            ("start", "b", "A", "b", "A", "c", "A", "end"),
            ("start", "b", "A", "b", "A", "end"),
            ("start", "b", "A", "b", "end"),
            ("start", "b", "A", "c", "A", "b", "A", "end"),
            ("start", "b", "A", "c", "A", "b", "end"),
            ("start", "b", "A", "c", "A", "c", "A", "end"),
            ("start", "b", "A", "c", "A", "end"),
            ("start", "b", "A", "end"),
            ("start", "b", "d", "b", "A", "c", "A", "end"),
            ("start", "b", "d", "b", "A", "end"),
            ("start", "b", "d", "b", "end"),
            ("start", "b", "end"),
        ]
    )
    actual = set(map(tuple, day.dfs(data, "start")))
    assert expected == actual


def test_example_103_paths():

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
    expected = 103
    actual = day.solve(data)
    assert expected == actual


def test_example_3509_paths():
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
    expected = 3509
    actual = day.solve(data)
    assert expected == actual
