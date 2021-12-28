#!/usr/bin/env python3

import pytest

import year2021.day24a as day


@pytest.mark.parametrize("input_number", list(range(10)))
def test_example_1(input_number):
    case = """
inp x
mul x -1
"""
    data = day.parse_input(case)
    alu = day.ALU(data)
    alu.run(iter([input_number]))
    assert alu.registers.x == -input_number


@pytest.mark.parametrize(
    "input_numbers,expected",
    [
        ([1, 1], 0),
        ([1, 2], 0),
        ([1, 3], 1),
        ([2, 4], 0),
        ([2, 5], 0),
        ([2, 6], 1),
        ([3, 7], 0),
        ([3, 8], 0),
        ([3, 9], 1),
    ],
)
def test_example_2(input_numbers, expected):
    case = """
inp z
inp x
mul z 3
eql z x
"""
    data = day.parse_input(case)
    alu = day.ALU(data)
    alu.run(iter(input_numbers))
    assert alu.registers.z == expected


@pytest.mark.parametrize(
    "input_number,expected",
    [(i, list(map(int, list(bin(i).split("0b")[-1].zfill(4))))) for i in range(10)],
)
def test_example_3(input_number, expected):
    case = """
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
"""
    data = day.parse_input(case)
    alu = day.ALU(data)
    alu.run(iter([input_number]))
    assert alu.registers.w == expected[0]
    assert alu.registers.x == expected[1]
    assert alu.registers.y == expected[2]
    assert alu.registers.z == expected[3]
