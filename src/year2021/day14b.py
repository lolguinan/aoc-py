#!/usr/bin/env python3

import collections
import re


Rules = dict[tuple[str, str], str]
ParsedInput = tuple[str, Rules]
Pairs = collections.Counter[tuple[str, str], int]
Counts = collections.Counter[str, int]


def parse_input(content: str) -> ParsedInput:
    template = re.findall(r"^\s*([A-Z]+)\s*$", content, flags=re.MULTILINE)

    rules = re.findall(
        r"\s*".join(["^", "([A-Z]{2})", "-", ">", "([A-Z]{1})", "$"]),
        content,
        flags=re.MULTILINE,
    )

    template = template[0]
    rules = {tuple(pair): elem for pair, elem in rules}

    return template, rules


def make_pairs(template: str) -> Pairs:
    pairs = [tuple(template[i : i + 2]) for i in range(len(template))]
    pairs = filter(lambda s: len(s) == 2, pairs)
    pairs = collections.Counter(pairs)
    return pairs


def apply_rules(pairs: Pairs, counts: Counts, rules: Rules) -> tuple[Pairs, Counts]:
    state = collections.Counter()

    for pair in pairs:
        if pair in rules:
            insert = rules[pair]
            left, right = pair
            state[(left, insert)] += pairs[pair]
            state[(insert, right)] += pairs[pair]
            counts[insert] += pairs[pair]
        else:
            state.update([pair])

    return state, counts


def solve(data: ParsedInput, max_steps: int) -> int:
    template, rules = data

    pairs = make_pairs(template)
    counts = collections.Counter(template)

    for _ in range(max_steps):
        pairs, counts = apply_rules(pairs, counts, rules)

    counts = counts.most_common()
    _, most_common = counts[0]
    _, least_common = counts[-1]

    return most_common - least_common


def main(runner=False):
    with open("inputs/014.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data, 40)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
