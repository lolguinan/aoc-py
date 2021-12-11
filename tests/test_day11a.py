#!/usr/bin/env python3

import pytest

import year2021.day11a as day


def test_neighbors():
    case = (5, 5)
    expected = [
        (4, 5),
        (4, 4),
        (5, 4),
        (6, 4),
        (6, 5),
        (6, 6),
        (5, 6),
        (4, 6),
    ]
    actual = day.neighbor_candidates(*case)
    assert expected == actual


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
    expected = 204
    actual = day.solve(data, 10)
    assert expected == actual
    expected = 1656
    actual = day.solve(data, 100)
    assert expected == actual
