#!/usr/bin/env python3

import pytest

import year2021.day25a as day


@pytest.mark.parametrize(
    "steps,expected",
    [
        (
            1,
            """
..vv>..
.......
>......
v.....>
>......
.......
....v..
""".strip(),
        ),
        (
            2,
            """
....v>.
..vv...
.>.....
......>
v>.....
.......
.......
""".strip(),
        ),
        (
            3,
            """
......>
..v.v..
..>v...
>......
..>....
v......
.......
""".strip(),
        ),
        (
            4,
            """
>......
..v....
..>.v..
.>.v...
...>...
.......
v......
""".strip(),
        ),
    ],
)
def test_example_1(steps, expected):
    case = """
...>...
.......
......>
v.....>
......>
.......
..vvv..
"""
    data = day.parse_input(case)
    state = data
    for step in range(steps):
        state = day.step_move(state)
    actual = day.render_grid(state)
    assert expected == actual


@pytest.mark.parametrize(
    "steps,expected",
    [
        (
            1,
            """
....>.>v.>
v.v>.>v.v.
>v>>..>v..
>>v>v>.>.v
.>v.v...v.
v>>.>vvv..
..v...>>..
vv...>>vv.
>.v.v..v.v
""".strip(),
        ),
        (
            2,
            """
>.v.v>>..v
v.v.>>vv..
>v>.>.>.v.
>>v>v.>v>.
.>..v....v
.>v>>.v.v.
v....v>v>.
.vv..>>v..
v>.....vv.
""".strip(),
        ),
        (
            3,
            """
v>v.v>.>v.
v...>>.v.v
>vv>.>v>..
>>v>v.>.v>
..>....v..
.>.>v>v..v
..v..v>vv>
v.v..>>v..
.v>....v..
""".strip(),
        ),
        (
            4,
            """
v>..v.>>..
v.v.>.>.v.
>vv.>>.v>v
>>.>..v>.>
..v>v...v.
..>>.>vv..
>.v.vv>v.v
.....>>vv.
vvv>...v..
""".strip(),
        ),
        (
            5,
            """
vv>...>v>.
v.v.v>.>v.
>.v.>.>.>v
>v>.>..v>>
..v>v.v...
..>.>>vvv.
.>...v>v..
..v.v>>v.v
v.v.>...v.
""".strip(),
        ),
        (
            10,
            """
..>..>>vv.
v.....>>.v
..v.v>>>v>
v>.>v.>>>.
..v>v.vv.v
.v.>>>.v..
v.v..>v>..
..v...>v.>
.vv..v>vv.
""".strip(),
        ),
        (
            20,
            """
v>.....>>.
>vv>.....v
.>v>v.vv>>
v>>>v.>v.>
....vv>v..
.v.>>>vvv.
..v..>>vv.
v.v...>>.v
..v.....v>
""".strip(),
        ),
        (
            30,
            """
.vv.v..>>>
v>...v...>
>.v>.>vv.>
>v>.>.>v.>
.>..v.vv..
..v>..>>v.
....v>..>v
v.v...>vv>
v.v...>vvv
""".strip(),
        ),
        (
            40,
            """
>>v>v..v..
..>>v..vv.
..>>>v.>.v
..>>>>vvv>
v.....>...
v.v...>v>>
>vv.....v>
.>v...v.>v
vvv.v..v.>
""".strip(),
        ),
        (
            50,
            """
..>>v>vv.v
..v.>>vv..
v.>>v>>v..
..>>>>>vv.
vvv....>vv
..v....>>>
v>.......>
.vv>....v>
.>v.vv.v..
""".strip(),
        ),
        (
            55,
            """
..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv...>..>
>vv.....>.
.>v.vv.v..
""".strip(),
        ),
        (
            56,
            """
..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv....>.>
>vv......>
.>v.vv.v..
""".strip(),
        ),
        (
            57,
            """
..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv.....>>
>vv......>
.>v.vv.v..
""".strip(),
        ),
        (
            58,
            """
..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv.....>>
>vv......>
.>v.vv.v..
""".strip(),
        ),
    ],
)
def test_example_2(steps, expected):
    case = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
    data = day.parse_input(case)
    state = data
    for step in range(steps):
        state = day.step_move(state)
    actual = day.render_grid(state)
    assert expected == actual


def test_example():
    case = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
    data = day.parse_input(case)
    expected = 58
    actual = day.solve(data)
    assert expected == actual
