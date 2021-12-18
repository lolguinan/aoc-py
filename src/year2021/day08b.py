#!/usr/bin/env python3

import functools
import itertools
import os


CORPUS = "abcdefg"

SEGMENTS = {
    0: "abcefg",  # len 6
    1: "cf",  # len 2
    2: "acdeg",  # len 5
    3: "acdfg",  # len 5
    4: "bcdf",  # len 4
    5: "abdfg",  # len 5
    6: "abdefg",  # len 6
    7: "acf",  # len 3
    8: "abcdefg",  # len 7
    9: "abcdfg",  # len 6
}


def parse_input(content: str) -> list[tuple[list[str], list[str]]]:
    rows = list(filter(None, map(str.strip, content.split(os.linesep))))
    rows = [list(map(str.strip, row.split("|"))) for row in rows]
    rows = [
        (
            a.split(),
            b.split(),
        )
        for a, b in rows
    ]
    return rows


def segment_to_digit(segment: str) -> int:
    for digit, letters in SEGMENTS.items():
        if set(letters) == set(segment):
            return digit
    raise Exception(f"Unknown segment: {segment}")


def apply_translation(patterns: list[str], translations: dict[str, str]) -> list[str]:
    return ["".join(translations[ch] for ch in pattern) for pattern in patterns]


@functools.cache
def get_all_translations() -> list[dict[str, str]]:
    translations = []
    for source in itertools.permutations(CORPUS):
        translations.append(dict(zip(source, CORPUS)))
    return translations


@functools.cache
def get_all_wire_permutations() -> list[set[str]]:
    groups = []
    for translations in get_all_translations():
        inverted = dict((v, k) for k, v in translations.items())
        groups.append(
            set(
                "".join(sorted(pattern))
                for pattern in apply_translation(SEGMENTS.values(), inverted)
            )
        )
    return groups


def deduce_rewire(patterns: list[str]) -> dict[str, str]:
    patterns = set("".join(sorted(pattern)) for pattern in patterns)

    precompute = list(zip(get_all_translations(), get_all_wire_permutations()))
    for translations, wire_group in precompute:
        if wire_group == patterns:
            return translations

    raise Exception("Invalid state.")


def solve(data: list[tuple[list[str], list[str]]]) -> int:
    total = 0
    for patterns, output in data:
        translations = deduce_rewire(patterns)
        resolved = apply_translation(output, translations)
        digits = list(map(segment_to_digit, resolved))
        digits = int("".join(map(str, digits)))
        total += digits
    return total


def main(runner=False):
    with open("inputs/year2021/008.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
