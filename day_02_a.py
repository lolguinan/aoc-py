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


def tests():
    case = '''
forward 5
down 5
forward 8
up 3
down 8
forward 2
'''
    case = parse_input(case)
    expected = (15, 10)
    actual = execute_plan(case)
    print(f'Case: {case}')
    print('Pass:', expected == actual)
    if expected != actual:
        print(f'Expected: {expected}, Actual: {actual}')


def main():
    print('Running tests...')
    tests()
    print()
    # return

    with open('inputs/002.txt') as fp:
        content = fp.read()

    commands = parse_input(content)
    x, y = execute_plan(commands)
    print(f'({x}, {y}) and {x} * {y} = {x * y}')


if __name__ == '__main__':
    main()
