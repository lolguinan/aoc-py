#!/usr/bin/env python3

import dataclasses
import os
import typing as T


def parse_input(content: str) -> list[list[str | int]]:
    instructions = []
    for line in filter(None, map(str.strip, content.split(os.linesep))):
        components = line.split()
        for i, c in enumerate(components):
            try:
                components[i] = int(c)
            except ValueError:
                pass
        instructions.append(components)
    return instructions


def check_instruction_repeats(instructions: list[list[str | int]]) -> dict:
    # convert instructions to symbolic form (no number literals)
    parsed = []
    for instruction in instructions:
        if len(instruction) == 2:
            op, a = instruction
            parsed.append([op, a])
        else:
            op, a, b = instruction
            if isinstance(b, int):
                b = "N"
            parsed.append([op, a, b])

    # find length of a section from first to second input
    section_length = 0
    for index, parse in enumerate(parsed):
        if index == 0:
            continue
        if parsed[index] == parsed[0]:
            section_length = index
            break

    # group into sections
    sections = []
    for index, parse in enumerate(parsed):
        if index == 0 or index % section_length == 0:
            sections.append([])
        sections[-1].append(parse)

    # compare sections
    for index in range(len(sections) - 1):
        if sections[index] != sections[index + 1]:
            raise Exception("Instruction sections do not repeat.")

    return {
        "total_instructions": len(instructions),
        "section_length": section_length,
        "total_sections": len(sections),
    }


@dataclasses.dataclass
class Variant:
    z_div: int
    x_add: int
    y_add: int


def resolve_implications(variants: list[Variant]):
    stack = []
    rules = []
    for curr_index, variant in enumerate(variants):
        match variant.z_div:
            case 1:
                stack.append(curr_index)
            case 26:
                # w[s[n]] = w[s[n - 1]] + y_add[s[n - 1]] + x_add[s[n]]
                prev_index = stack.pop()
                rules.append(
                    [
                        curr_index,
                        prev_index,
                        variants[prev_index].y_add + variants[curr_index].x_add,
                    ]
                )
            case _:
                raise Exception(f"Invalid variant: {variant}")

    ws = {}
    for w1, w0, delta in rules:
        if delta > 0:
            right = 1
            left = right + delta
        else:
            left = 1
            right = abs(delta) + 1
        ws[w1] = left
        ws[w0] = right

    ws = [ws[i] for i in range(len(variants))]

    return "".join(map(str, ws))


def solve(data: list[list[str | int]]) -> str:
    check = check_instruction_repeats(data)

    n = check["section_length"]
    groups = [data[i : i + n] for i in range(0, len(data), n)]

    variants = [Variant(group[4][-1], group[5][-1], group[15][-1]) for group in groups]

    return resolve_implications(variants)


def main(runner=False):
    with open("inputs/year2021/024.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
