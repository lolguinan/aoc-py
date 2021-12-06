#!/usr/bin/env python3

import year2021.day01b as day


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
    expected = 5
    actual = day.count_depth_increases(day.sums_in_window(case))
    assert expected == actual
