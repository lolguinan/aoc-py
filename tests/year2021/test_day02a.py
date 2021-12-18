#!/usr/bin/env python3

import year2021.day02a as day


def test_example():
    case = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""
    case = day.parse_input(case)
    expected = (15, 10)
    actual = day.execute_plan(case)
    assert expected == actual
