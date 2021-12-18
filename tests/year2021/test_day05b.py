#!/usr/bin/env python3

import year2021.day05b as day


def test_example():
    case = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
    data = day.parse_input(case)
    expected = 12
    actual = day.solve(data)
    assert expected == actual
