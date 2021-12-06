#!/usr/bin/env python3

import os


def parse_input(content: str) -> list[tuple[str, int]]:
    return [
        (
            a,
            int(b),
        )
        for a, b in map(
            str.split, filter(None, map(str.strip, content.split(os.linesep)))
        )
    ]


def execute_plan(commands: list[tuple[str, int]]) -> tuple[int, int]:
    x = y = aim = 0
    for command, value in commands:
        match command:
            case "forward":
                x += value
                y += value * aim
            case "down":
                aim += value
            case "up":
                aim -= value
            case _:
                raise Exception(f"Unknown command: {command}")
    return x, y


def main():
    with open("inputs/002.txt") as fp:
        content = fp.read()

    commands = parse_input(content)
    x, y = execute_plan(commands)
    print(f"({x}, {y}) and {x} * {y} = {x * y}")


if __name__ == "__main__":
    main()
