#!/usr/bin/env python3

import year2021.day06a as day


def test_example_18_days():
    case = """
3,4,3,1,2
"""
    data = day.parse_input(case)
    expected = 26
    actual = day.solve(data, 18)
    assert expected == actual


def test_example_80_days():
    case = """
3,4,3,1,2
"""
    data = day.parse_input(case)
    expected = 5934
    actual = day.solve(data, 80)
    assert expected == actual
