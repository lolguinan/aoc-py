#!/usr/bin/env python3

import dataclasses
import os
import typing as T

import colorama


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


@dataclasses.dataclass
class Vector4:
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0


class ALU:
    def __init__(self, program: list[list[str | int]]):
        self.program = program
        self.registers = Vector4()
        self.prev_registers = Vector4()
        self.index = 0

    def read(self, register: str) -> int:
        return getattr(self.registers, register)

    def write(self, register: str, value: int):
        setattr(self.registers, register, value)

    def resolve(self, maybe_register: str | int) -> int:
        if isinstance(maybe_register, str):
            return self.read(maybe_register)
        return maybe_register

    def run(self, input_stream: T.Iterable[int]):
        for index, instruction in enumerate(self.program):
            self.prev_registers = dataclasses.replace(self.registers)
            self.index = index
            match instruction:
                case ["inp", a]:
                    v = next(input_stream)
                    self.write(a, v)
                case ["add", a, b]:
                    v = self.read(a) + self.resolve(b)
                    self.write(a, v)
                case ["mul", a, b]:
                    v = self.read(a) * self.resolve(b)
                    self.write(a, v)
                case ["div", a, b]:
                    v = self.read(a) // self.resolve(b)
                    self.write(a, v)
                case ["mod", a, b]:
                    v = self.read(a) % self.resolve(b)
                    self.write(a, v)
                case ["eql", a, b]:
                    v = int(self.read(a) == self.resolve(b))
                    self.write(a, v)
                case _:
                    raise Exception(f"Unknown instruction: {instruction}")
            self.output_step(instruction)

    def output_step(self, instruction: list[str | int]):
        def style(value: T.Any, *mods: str) -> str:
            return "".join(mods) + str(value) + colorama.Style.RESET_ALL

        fmt = "  ".join(
            [
                # index
                style(
                    "{:>3}",
                    colorama.Fore.CYAN,
                    colorama.Style.BRIGHT,
                ),
                # instruction
                "[ {} ]".format(
                    style(
                        "{:>3} {:>1} {:>3}",
                        colorama.Fore.YELLOW,
                        colorama.Style.BRIGHT,
                    )
                ),
                # registers
                "[ {} ]".format(
                    "".join(
                        [
                            style("w", colorama.Fore.RED),
                            ":{:>12}, ",
                            style("x", colorama.Fore.RED),
                            ":{:>12}, ",
                            style("y", colorama.Fore.RED),
                            ":{:>12}, ",
                            style("z", colorama.Fore.RED),
                            ":{:>12}",
                        ]
                    )
                ),
            ]
        )

        def register_repr(name: str) -> str:
            reg_change = colorama.Fore.GREEN + colorama.Style.BRIGHT
            reg_no_change = colorama.Style.DIM
            prev = getattr(self.prev_registers, name)
            curr = getattr(self.registers, name)
            if prev == curr:
                return style("{:>12}".format(curr), reg_no_change)
            else:
                return style("{:>12}".format(curr), reg_change)

        row = [
            self.index,
            *[instruction[i] if i < len(instruction) else "" for i in range(3)],
            *[
                register_repr("w"),
                register_repr("x"),
                register_repr("y"),
                register_repr("z"),
            ],
        ]

        print(fmt.format(*row))


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


# Each section of input looks like:
#
# inp w
# mul x 0
# add x z
# mod x 26
# div z ZDIV
# add x XADD
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y YADD
# mul y x
# add z y
#
# Evaluating:
#
# [ 0] [inp w     ] w : inp
# [ 1] [mul x 0   ] x0 : 0
# [ 2] [add x z   ] x0 : z0
# [ 3] [mod x 26  ] x0 : z0 % 26
# [ 4] [div z ZDIV] z1 : z0 // ZDIV
# [ 5] [add x XADD] x1 : (z0 % 26) + XADD
# [ 6] [eql x w   ] x1 : ((z0 % 26) + XADD) == w
# [ 7] [eql x 0   ] x1 : (((z0 % 26) + XADD) == w) == 0
# [ 8] [mul y 0   ] y0 : 0
# [ 9] [add y 25  ] y0 : 25
# [10] [mul y x   ] y0 : 25 * {0,1}
# [11] [add y 1   ] y0 : (25 * {0,1}) + 1
# [12] [mul z y   ] z2 : (z0 // ZDIV) * ((25 * {0,1}) + 1)
# [13] [mul y 0   ] y1 : 0
# [14] [add y w   ] y1 : w
# [15] [add y YADD] y1 : w + YADD
# [16] [mul y x   ] y1 : (w + YADD) * {0,1}
# [17] [add z y   ] z3 : ((z0 // ZDIV) * ((25 * {0,1}) + 1)) + ((w + YADD) * {0,1})
#
# x == w => x = 0
# [10] [mul y x   ] y0 : 0
# [11] [add y 1   ] y0 : 1
# [12] [mul z y   ] z2 : z0 // ZDIV
# [13] [mul y 0   ] y1 : 0
# [14] [add y w   ] y1 : w
# [15] [add y YADD] y1 : w + YADD
# [16] [mul y x   ] y1 : 0
# [17] [add z y   ] z3 : z0 // ZDIV
#
# x != w => x = 1
# [10] [mul y x   ] y0 : 25
# [11] [add y 1   ] y0 : 26
# [12] [mul z y   ] z2 : (z0 // ZDIV) * 26
# [13] [mul y 0   ] y1 : 0
# [14] [add y w   ] y1 : w
# [15] [add y YADD] y1 : w + YADD
# [16] [mul y x   ] y1 : w + YADD
# [17] [add z y   ] z3 : ((z0 // ZDIV) * 26) + (w + YADD)
#
# This input:
#
# IDX , ZDIV , XADD , YADD
# 0   , 1    , 11   , 5
# 1   , 1    , 13   , 5
# 2   , 1    , 12   , 1
# 3   , 1    , 15   , 15
# 4   , 1    , 10   , 2
# 5   , 26   , -1   , 2
# 6   , 1    , 14   , 5
# 7   , 26   , -8   , 8
# 8   , 26   , -7   , 14
# 9   , 26   , -8   , 12
# 10  , 1    , 11   , 7
# 11  , 26   , -2   , 14
# 12  , 26   , -2   , 13
# 13  , 26   , -13  , 6


def apply_section(w, z, z_div, x_add, y_add):
    x = (z % 26) + x_add
    z = z // z_div  # z_div is 1 or 26

    if x != w:
        z = (z * 26) + (w + y_add)

    # div, mod, and mul by 26 (implies base-26)
    # when z_div == 26
    # * x contains last "digit" of z decreased (-x_add)
    # * z is shifted (drop last digit)
    # * x == w is possible here
    # when z_div == 1
    # * x contains last "digit" of z increased (+x_add)
    # * x increase always greater than one input digit (x_add >= 10)
    # * x == w is not possible here
    # * shift and add a "digit" to z (w + y_add)

    # z-digit interactions are not sequential
    # * z_div == 1 adds a digit each encounter
    # * z_div == 26 removes a digit each encounter
    # * multiple z_div == 1 add multiple digits
    # * single z_div == 26 removes single digit
    # => stack

    # add a digit by (w + y_add) only when z_div == 1
    # check to not add a digit by (z % 26) + x_add == w
    # for x == w to be true (don't add digit), based on stack:
    # w[s[n]] = z[s[n - 1]] + x_add[s[n]]
    # where:
    # z[s[n]] = w[s[n]] + y_add[s[n]]
    # so:
    # w[s[n]] = w[s[n - 1]] + y_add[s[n - 1]] + x_add[s[n]]

    return z


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
            left = 9
            right = left - delta
        else:
            right = 9
            left = left + delta
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
