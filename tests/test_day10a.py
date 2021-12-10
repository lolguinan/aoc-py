#!/usr/bin/env python3

import pytest

import year2021.day10a as day


@pytest.mark.parametrize(
    "chunks",
    [
        "()",
        "[]",
        "([])",
        "{()()()}",
        "<([{}])>",
        "[<>({}){}[([])<>]]",
        "(((((((((())))))))))",
    ],
)
def test_example_chunks_legal(chunks):
    data = day.parse_input(chunks)
    expected = day.Status.LEGAL
    actual = day.parse(data[0])
    assert expected == actual.status


@pytest.mark.parametrize(
    "chunks,expected",
    [
        # from example description
        ("(]", day.ParseResult(day.Status.CORRUPTED, 1, ")", "]")),
        ("{()()()>", day.ParseResult(day.Status.CORRUPTED, 7, "}", ">")),
        ("(((()))}", day.ParseResult(day.Status.CORRUPTED, 7, ")", "}")),
        ("<([]){()}[{}])", day.ParseResult(day.Status.CORRUPTED, 13, ">", ")")),
        # from example input
        (
            "{([(<{}[<>[]}>{[]{[(<()>",
            day.ParseResult(day.Status.CORRUPTED, 12, "]", "}"),
        ),
        ("[[<[([]))<([[{}[[()]]]", day.ParseResult(day.Status.CORRUPTED, 8, "]", ")")),
        ("[{[{({}]{}}([{[{{{}}([]", day.ParseResult(day.Status.CORRUPTED, 7, ")", "]")),
        ("[<(<(<(<{}))><([]([]()", day.ParseResult(day.Status.CORRUPTED, 10, ">", ")")),
        ("<{([([[(<>()){}]>(<<{{", day.ParseResult(day.Status.CORRUPTED, 16, "]", ">")),
    ],
)
def test_example_chunks_illegal(chunks, expected):
    data = day.parse_input(chunks)
    actual = day.parse(data[0])
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
    expected = 26397
    actual = day.solve(data)
    assert expected == actual
