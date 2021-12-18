#!/usr/bin/env python3

import pytest

import year2021.day07a as day


@pytest.mark.parametrize(
    "case,pos,cost",
    [
        ("16,1,2,0,4,2,7,1,2,14", 2, 37),
        ("16,1,2,0,4,2,7,1,2,14", 1, 41),
        ("16,1,2,0,4,2,7,1,2,14", 3, 39),
        ("16,1,2,0,4,2,7,1,2,14", 10, 71),
    ],
)
def test_example(case, pos, cost):
    data = day.parse_input(case)
    expected = (pos, cost)
    actual = (pos, day.get_costs(data).get(pos, None))
    assert expected == actual
