#!/usr/bin/env python3

import pytest

import year2021.day10b as day


@pytest.mark.parametrize(
    "chunks,completion,score",
    [
        ("[({(<(())[]>[[{[]{<()<>>", "}}]])})]", 288957),
        ("[(()[<>])]({[<{<<[]>>(", ")}>]})", 5566),
        ("(((({<>}<{<{<>}{[]{[]{}", "}}>}>))))", 1480781),
        ("{<[[]]>}<{[{[{[]{()[[[]", "]]}}]}]}>", 995444),
        ("<{([{{}}[<[[[<>{}]]]>[]]", "])}>", 294),
    ],
)
def test_example_completion_scores(chunks, completion, score):
    data = day.parse_input(chunks)
    expected = completion
    actual = "".join(day.parse_incomplete(data[0]))
    assert expected == actual
    expected = score
    actual = day.get_score(actual)
    assert expected == actual


def test_example():
    case = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
    data = day.parse_input(case)
    expected = 288957
    actual = day.solve(data)
    assert expected == actual
