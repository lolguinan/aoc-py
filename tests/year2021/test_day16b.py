#!/usr/bin/env python3

import pytest

import year2021.day16b as day


@pytest.mark.parametrize(
    "case,expected",
    [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ],
)
def test_examples(case, expected):
    data = day.convert_hex_to_bin(day.parse_input(case))
    actual = day.solve(data)
    assert expected == actual
