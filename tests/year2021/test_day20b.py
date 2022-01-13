#!/usr/bin/env python3

import year2021.day20a as day


EXAMPLE = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


def test_example_render_0_step():
    algo, image = day.parse_input(EXAMPLE)
    expected = """
#..#.
#....
##..#
..#..
..###
    """.strip()
    actual = day.render_image(image)
    assert expected == actual


def test_example_render_1_step():
    algo, image = day.parse_input(EXAMPLE)
    expected = """
.##.##.
#..#.#.
##.#..#
####..#
.#..##.
..##..#
...#.#.
""".strip()
    image = day.apply_enhancement(algo, image, day.Pixel.DARK)
    actual = day.render_image(image)
    assert expected == actual


def test_example_render_2_step():
    algo, image = day.parse_input(EXAMPLE)
    expected = """
.......#.
.#..#.#..
#.#...###
#...##.#.
#.....#.#
.#.#####.
..#.#####
...##.##.
....###..
""".strip()
    image = day.apply_enhancement(algo, image, day.Pixel.DARK)
    image = day.apply_enhancement(algo, image, day.Pixel.DARK)
    actual = day.render_image(image)
    assert expected == actual


def test_example():
    data = day.parse_input(EXAMPLE)
    expected = 3351
    actual = day.solve(data, rounds=50)
    assert expected == actual
