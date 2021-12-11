#!/usr/bin/env python3

import math

import pytest

import year2021.day11b as day


def test_example():
    case = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
    data = day.parse_input(case)
    expected = 195
    actual = day.solve(data, math.inf)
    assert expected == actual
