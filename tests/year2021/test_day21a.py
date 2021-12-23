#!/usr/bin/env python3

import pytest

import year2021.day21a as day


def test_die():
    die = day.DeterministicDie(100)
    expected = list(range(1, 101)) + list(range(1, 101))
    actual = [die.roll() for _ in range(200)]
    assert expected == actual


@pytest.mark.parametrize(
    "turns,expected_positions,expected_scores",
    [
        (1, {1: 10, 2: 3}, {1: 10, 2: 3}),
        (2, {1: 4, 2: 6}, {1: 14, 2: 9}),
        (3, {1: 6, 2: 7}, {1: 20, 2: 16}),
        (4, {1: 6, 2: 6}, {1: 26, 2: 22}),
    ],
)
def test_example_turns(turns, expected_positions, expected_scores):
    case = """
Player 1 starting position: 4
Player 2 starting position: 8
"""
    start_positions = day.parse_input(case)
    positions = {player: pos for player, pos in start_positions.items()}
    scores = {player: 0 for player in positions}
    die = day.DeterministicDie(100)
    for turn in range(turns):
        day.play_round(1000, positions, scores, die)
    assert positions == expected_positions
    assert scores == expected_scores


def test_example():
    case = """
Player 1 starting position: 4
Player 2 starting position: 8
"""
    data = day.parse_input(case)
    expected = 739785
    actual = day.solve(1000, data)
    assert expected == actual
