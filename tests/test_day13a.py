#!/usr/bin/env python3

import year2021.day13a as day


def test_example():
    case = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""
    data = day.parse_input(case)
    expected = 17
    actual = day.solve(data, 1)
    assert expected == actual
