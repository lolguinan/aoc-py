#!/usr/bin/env python3

import year2021.day09b as day


def test_example_basin_top_left():
    case = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
    data = day.parse_input(case)
    expected = set(
        [
            (0, 0),
            (1, 0),
            (0, 1),
        ]
    )
    actual = day.flood_basin(data, day.BOUNDARY, 1, 0)
    assert expected == actual


def test_example_basin_top_right():
    case = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
    data = day.parse_input(case)
    expected = set(
        [
            (5, 0),
            (6, 0),
            (7, 0),
            (8, 0),
            (9, 0),
            (6, 1),
            (8, 1),
            (9, 1),
            (9, 2),
        ]
    )
    actual = day.flood_basin(data, day.BOUNDARY, 9, 0)
    assert expected == actual


def test_example_basin_middle():
    case = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
    data = day.parse_input(case)
    expected = set(
        [
            (2, 1),
            (3, 1),
            (4, 1),
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
            (0, 3),
            (1, 3),
            (2, 3),
            (3, 3),
            (4, 3),
            (1, 4),
        ]
    )
    actual = day.flood_basin(data, day.BOUNDARY, 2, 2)
    assert expected == actual


def test_example_basin_bottom_right():
    case = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
    data = day.parse_input(case)
    expected = set(
        [
            (7, 2),
            (6, 3),
            (7, 3),
            (8, 3),
            (5, 4),
            (6, 4),
            (7, 4),
            (8, 4),
            (9, 4),
        ]
    )
    actual = day.flood_basin(data, day.BOUNDARY, 6, 4)
    assert expected == actual


def test_example():
    case = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
    data = day.parse_input(case)
    expected = 1134
    actual = day.solve(data)
    assert expected == actual
