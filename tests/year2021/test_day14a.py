#!/usr/bin/env python3

import year2021.day14a as day


def test_example_step_output():
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
    template, rules = data
    link_root = day.Node.build(template)
    expected = [
        "NNCB",
        "NCNBCHB",
        "NBCCNBBBCBHCB",
        "NBBBCNCCNBBNBNBBCHBHHBCHB",
        "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB",
    ]
    assert expected[0] == str(link_root)
    for result in expected[1:]:
        link_root = day.apply_rules(link_root, rules)
        actual = str(link_root)
        assert result == actual


def test_example():
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
