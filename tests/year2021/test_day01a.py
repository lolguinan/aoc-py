#!/usr/bin/env python3

import year2021.day01a as day


def test_example():
    case = """
199
200
208
210
200
207
240
269
260
263
"""
    case = day.parse_input(case)
    expected = 7
    actual = day.count_depth_increases(case)
    assert expected == actual
