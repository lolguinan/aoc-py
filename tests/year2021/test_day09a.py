#!/usr/bin/env python3

import year2021.day09a as day


def test_example():
    case = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
    data = day.parse_input(case)
    expected = 15
    actual = day.solve(data)
    assert expected == actual
