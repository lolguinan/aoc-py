#!/usr/bin/env python3

import pytest

import year2021.day07b as day


@pytest.mark.parametrize(
    "start,stop,cost",
    [
        (16, 5, 66),
        (1, 5, 10),
        (2, 5, 6),
        (0, 5, 15),
        (4, 5, 1),
        (2, 5, 6),
        (7, 5, 3),
        (1, 5, 10),
        (2, 5, 6),
        (14, 5, 45),
    ],
)
def test_example_step_cost(start, stop, cost):
    expected = cost
    actual = day.get_move_cost(day.get_step_count(start, stop))
    assert expected == actual


@pytest.mark.parametrize(
    "case,pos,cost",
    [
        ("16,1,2,0,4,2,7,1,2,14", 5, 168),
        ("16,1,2,0,4,2,7,1,2,14", 2, 206),
    ],
)
def test_example_cheapest(case, pos, cost):
    data = day.parse_input(case)
    expected = (pos, cost)
    actual = (pos, day.get_costs(data).get(pos, None))
    assert expected == actual
