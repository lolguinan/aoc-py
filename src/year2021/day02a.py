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
        if command == 'forward':
            x += value
        elif command == 'down':
            y += value
        elif command == 'up':
            y -= value
        else:
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
