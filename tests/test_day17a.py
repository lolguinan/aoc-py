#!/usr/bin/env python3

import pytest

import year2021.day17a as day


@pytest.mark.parametrize(
    "vx,vy",
    [
        (7, 2),
        (6, 3),
        (9, 0),
    ],
)
def test_examples_hit_target(vx, vy):
    case = """
target area: x=20..30, y=-10..-5
    """
    data = day.parse_input(case)
    expected = True
    actual, _ = day.launch_probe(data, day.Vector2(vx, vy))
    assert expected == actual


def test_example_miss_target():
    case = """
target area: x=20..30, y=-10..-5
    """
    data = day.parse_input(case)
    expected = False
    actual, _ = day.launch_probe(data, day.Vector2(17, -4))
    assert expected == actual


def test_example():
    case = """
target area: x=20..30, y=-10..-5
    """
    data = day.parse_input(case)
    expected = 45
    actual = day.solve(data)
    assert expected == actual
