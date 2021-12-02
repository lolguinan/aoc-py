#!/usr/bin/env python3

import os


def parse_input(content):
    return list(map(int, filter(None, map(str.strip,
        content.split(os.linesep)))))


def sums_in_window(depths, window_length=3):
    windows = [
        depths[index: index + window_length]
        for index in range(len(depths))
    ]
    windows = [
        window for window in windows
        if len(window) == window_length
    ]
    return list(map(sum, windows))


def count_depth_increases(depths):
    increases = 0
    for index in range(0, len(depths) - 1):
        a = depths[index]
        b = depths[index + 1]
        if b > a:
            increases += 1
    return increases


def tests():
    case = '''
199
200
208
210
200
207
240
269
260
263
'''
    case = parse_input(case)
    expected = 5
    actual = count_depth_increases(sums_in_window(case))
    print(f'Case: {case}')
    print('Pass:', expected == actual)
    if expected != actual:
        print(f'Expected: {expected}, Actual: {actual}')


def main():
    print('Running tests...')
    tests()
    # return

    print()

    with open('inputs/001.txt') as fp:
        content = fp.read()

    depths = parse_input(content)
    print(count_depth_increases(sums_in_window(depths)))


if __name__ == '__main__':
    main()
