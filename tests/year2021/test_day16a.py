#!/usr/bin/env python3

import pytest

import year2021.day16a as day


def test_example_hex_to_bin():
    case = """
D2FE28
"""
    data = day.parse_input(case)
    expected = "110100101111111000101000"
    actual = day.convert_hex_to_bin(data)
    assert expected == actual


def test_example_literal_value():
    case = """
D2FE28
"""
    data = day.convert_hex_to_bin(day.parse_input(case))
    expected = 2021
    _, actual = day.read_packet(data)
    actual = actual.value
    assert expected == actual


def test_example_operator_length_type_0_two_subs():
    case = """
38006F45291200
"""
    data = day.convert_hex_to_bin(day.parse_input(case))
    expected = [10, 20]
    _, actual = day.read_packet(data)
    actual = [child.value for child in actual.children]
    assert expected == actual


def test_example_operator_length_type_1_three_subs():
    case = """
EE00D40C823060
"""
    data = day.convert_hex_to_bin(day.parse_input(case))
    expected = [1, 2, 3]
    _, actual = day.read_packet(data)
    actual = [child.value for child in actual.children]
    assert expected == actual


@pytest.mark.parametrize(
    "case,version_sum",
    [
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ],
)
def test_examples(case, version_sum):
    data = day.convert_hex_to_bin(day.parse_input(case))
    expected = version_sum
    actual = day.solve(data)
    assert expected == actual
