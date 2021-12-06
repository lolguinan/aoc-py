#!/usr/bin/env python3

import year2021.day03a as day


def test_example():
    case = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""
    case = day.parse_input(case)
    expected = 198
    actual = day.solve(case)
    assert expected == actual
