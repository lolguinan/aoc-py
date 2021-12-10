#!/usr/bin/env python3

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


def get_segment_activations(patterns: list[str]) -> set[tuple[int]]:
    return set(
        [tuple([int(letter in pattern) for letter in CORPUS]) for pattern in patterns]
    )


def render_activation_matrix(patterns: list[str]) -> str:
    return os.linesep.join(
        [
            ",".join([str(col) if col else " " for col in row])
            for row in get_segment_activations(patterns)
        ]
    )


def apply_translation(patterns: list[str], translations: dict[str, str]) -> list[str]:
    return ["".join(translations[ch] for ch in pattern) for pattern in patterns]


def deduce_rewire(patterns: list[str]) -> dict[str, str]:
    required_activations = get_segment_activations(SEGMENTS.values())

    for source in itertools.permutations(CORPUS):
        translations = dict(zip(source, CORPUS))

        candidate_activations = get_segment_activations(
            apply_translation(patterns, translations)
        )

        if required_activations == candidate_activations:
            return translations


def solve(data: list[tuple[list[str], list[str]]]) -> int:
    total = 0
    for patterns, output in data:
        translations = deduce_rewire(patterns)
        resolved = apply_translation(output, translations)
        digits = list(map(segment_to_digit, resolved))
        digits = int("".join(map(str, digits)))
        total += digits
    return total


def main():
    with open("inputs/008.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    print(answer)


if __name__ == "__main__":
    main()
