#!/usr/bin/env python3

import year2021.day15a as day


def test_example_path():
    case = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
    data = day.parse_input(case)
    expected = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (5, 2),
        (6, 2),
        (6, 3),
        (7, 3),
        (7, 4),
        # example highlighted path is "a path with the lowest total"
        # (7, 5),
        (8, 4),
        (8, 5),
        (8, 6),
        (8, 7),
        (8, 8),
        (9, 8),
        (9, 9),
    ]
    actual = day.dijkstra(data, (0, 0), (9, 9))
    assert expected == actual


def test_example():
    case = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
    data = day.parse_input(case)
    expected = 40
    actual = day.solve(data)
    assert expected == actual
