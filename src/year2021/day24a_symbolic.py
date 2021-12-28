#!/usr/bin/env python3

from __future__ import annotations
import dataclasses
import os
import pprint
import typing as T

import colorama
import sympy


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
        self.r_audit = {field.name: [] for field in dataclasses.fields(self.registers)}
        self.w_audit = {field.name: [] for field in dataclasses.fields(self.registers)}

    def read(self, register: str) -> int:
        self.r_audit[register].append(self.index)
        return getattr(self.registers, register)

    def write(self, register: str, value: int):
        self.w_audit[register].append(self.index)
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


def check_instruction_repeats(instructions: list[list[str | int]]) -> None:
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

    print("total instructions:", len(instructions))
    print("section length:", section_length)
    print("total sections:", len(sections))

    # compare sections
    for index in range(len(sections) - 1):
        if sections[index] != sections[index + 1]:
            raise Exception("Instruction sections do not repeat.")


@dataclasses.dataclass
class Op2:
    op: str
    a: str


@dataclasses.dataclass
class Op3:
    op: str
    a: str
    b: str | int


@dataclasses.dataclass
class Expr:
    op: str
    left: Expr | str
    right: Expr | str


def to_symbolic_tree(instruction_group: list[list[str | int]]):
    tree = []
    # n = 'a'

    last_write_to = None
    for instruction in instruction_group:
        cls = Op2 if len(instruction) == 2 else Op3
        op = cls(*instruction)
        # if cls == Op3 and isinstance(op.b, int):
        #     # op.b = 'N' + n
        #     n = chr(ord(n) + 1)
        if last_write_to is None or op.a != last_write_to:
            tree.append([])
        tree[-1].append(op)
        last_write_to = op.a

    # pprint.pprint(tree)

    refs = dataclasses.asdict(Vector4())
    exprs = {}
    for group in tree:
        # pprint.pprint(group)

        # when going through here, or maybe as a replacement step after,
        # each subsequent group has to refer to the previous iteration
        # of x, y, z
        # x0, y0, z0 = whatever was in those registers at the start
        # of this instruction group

        seen = set()

        e = None
        for op in group:
            if isinstance(op, Op2):
                continue
            a, b = op.a, op.b
            seen.add(a[0])
            if a[0] in refs:
                a = f"{a[0]}{refs[a[0]]}"
            # if len(b) == 1:
            if isinstance(b, str):
                if b[0] in refs:
                    b = f"{b[0]}{refs[b[0]]}"
            if e is None:
                e = Expr(op.op, a, b)
                continue
            e = Expr(op.op, e, b)

        if e is not None:
            key = f"{group[0].a}{refs[group[0].a[0]] + 1}"
            exprs[key] = e

        for ref in seen:
            if ref in refs:
                refs[ref] += 1

    pp = pprint.PrettyPrinter(indent=4)
    for expr in exprs:
        print(expr, "=", pp.pformat(exprs[expr]))

    def substitute(expr: Expr) -> Expr:
        if isinstance(expr, int):
            return
        if isinstance(expr.left, str):
            if expr.left in exprs:
                expr.left = exprs[expr.left]
        else:
            substitute(expr.left)
        if isinstance(expr.right, str):
            if expr.right in exprs:
                expr.right = exprs[expr.right]
        else:
            substitute(expr.right)

    for expr in exprs:
        substitute(exprs[expr])

    # print()
    # for expr in exprs:
    #     print(expr, '=', pp.pformat(exprs[expr]))

    def sexpr(expr: Expr | str | int) -> list:
        if isinstance(
            expr,
            (
                str,
                int,
            ),
        ):
            return expr
        return [expr.op, sexpr(expr.left), sexpr(expr.right)]

    print("=" * 80)
    pprint.pprint(exprs["z3"])
    pprint.pprint(sexpr(exprs["z3"]))

    op_trans = {
        "add": "+",
        "mul": "*",
        "div": "//",
        "mod": "%",
        "eql": "==",
    }

    def infix(expr: Expr | str | int) -> str:
        if isinstance(
            expr,
            (
                str,
                int,
            ),
        ):
            return expr
        if expr.op == "eql":
            return "".join(
                map(
                    str,
                    [
                        "(",
                        "(",
                        infix(expr.left),
                        " ",
                        op_trans[expr.op],
                        " ",
                        infix(expr.right),
                        ")" " and 1 or 0" ")",
                    ],
                )
            )
        else:
            return "".join(
                map(
                    str,
                    [
                        "(",
                        infix(expr.left),
                        " ",
                        op_trans[expr.op],
                        " ",
                        infix(expr.right),
                        ")",
                    ],
                )
            )

    # print(infix(exprs['z3']))

    # TODO: sympy doesn't like the ==s
    # TypeError: unsupported operand type(s) for *: 'Add' and 'bool'
    # wonder if "and 1 or 0" would work?

    print("=" * 80)
    last = sorted(exprs)[-1]

    w0, x0, y0, z0 = sympy.symbols("w0 x0 y0 z0")
    expr = infix(exprs[last])
    print(last, "=", expr)
    expr = eval(expr)
    print(last, "=", expr)
    print()

    # XXX: This can't be entirely correct because the last group:
    # z3 = w0 + 26*floor(z0/26) + 6
    # and 26 * z0 / 26 = z0, so no reduction.


def solve(data: list[list[str | int]]):
    alu = ALU(data)
    alu.run(iter(map(int, str(13579246899999))))


def main(runner=False):
    with open("inputs/year2021/024.txt") as fp:
        content = fp.read()

    data = parse_input(content)

    check_instruction_repeats(data)

    n = 18
    groups = [data[i : i + n] for i in range(0, len(data), n)]

    to_symbolic_tree(groups[-1])
    # for group in groups:
    #     to_symbolic_tree(group)

    return

    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
