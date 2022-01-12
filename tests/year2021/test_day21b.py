#!/usr/bin/env python3

import year2021.day21b as day


def test_example():
    case = """
Player 1 starting position: 4
Player 2 starting position: 8
"""
    data = day.parse_input(case)
    expected = 444356092776315
    actual = day.solve(data)
    assert expected == actual
