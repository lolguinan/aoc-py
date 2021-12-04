#!/usr/bin/env python3

import os


def parse_input(content):
    return [
        [a, int(b)] for a, b in
        map(str.split, filter(None, map(str.strip,
            content.split(os.linesep))))
    ]


def execute_plan(commands):
    x = y = 0
    for command, value in commands:
        match command:
            case 'forward':
                x += value
            case 'down':
                y += value
            case 'up':
                y -= value
            case _:
                raise Exception(f'Unknown command: {command}')
    return x, y


def main():
    with open('inputs/002.txt') as fp:
        content = fp.read()

    commands = parse_input(content)
    x, y = execute_plan(commands)
    print(f'({x}, {y}) and {x} * {y} = {x * y}')


if __name__ == '__main__':
    main()
