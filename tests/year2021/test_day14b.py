#!/usr/bin/env python3

import pytest

import year2021.day14b as day


@pytest.mark.parametrize(
    "template,expected",
    [
        (
            "NNCB",
            {
                ("N", "N"): 1,
                ("N", "C"): 1,
                ("C", "B"): 1,
            },
        ),
        (
            "NCNBCHB",
            {
                ("N", "C"): 1,
                ("C", "N"): 1,
                ("N", "B"): 1,
                ("B", "C"): 1,
                ("C", "H"): 1,
                ("H", "B"): 1,
            },
        ),
        (
            "NBCCNBBBCBHCB",
            {
                ("N", "B"): 2,
                ("B", "C"): 2,
                ("C", "C"): 1,
                ("C", "N"): 1,
                ("B", "B"): 2,
                ("C", "B"): 2,
                ("B", "H"): 1,
                ("H", "C"): 1,
            },
        ),
        (
            "NBBBCNCCNBBNBNBBCHBHHBCHB",
            {
                ("N", "B"): 4,
                ("B", "B"): 4,
                ("B", "C"): 3,
                ("C", "N"): 2,
                ("N", "C"): 1,
                ("C", "C"): 1,
                ("B", "N"): 2,
                ("C", "H"): 2,
                ("H", "B"): 3,
                ("B", "H"): 1,
                ("H", "H"): 1,
            },
        ),
    ],
)
def test_make_pairs(template, expected):
    actual = day.make_pairs(template)
    assert expected == actual


def test_example_10_steps():
    case = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
    data = day.parse_input(case)
    expected = 1588
    actual = day.solve(data, 10)
    assert expected == actual


def test_example_40_steps():
    case = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
    data = day.parse_input(case)
    expected = 2188189693529
    actual = day.solve(data, 40)
    assert expected == actual
