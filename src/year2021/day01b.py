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


def main():
    with open('inputs/001.txt') as fp:
        content = fp.read()

    depths = parse_input(content)
    windowed_depths = sums_in_window(depths)
    increases = count_depth_increases(windowed_depths)
    print(increases)


if __name__ == '__main__':
    main()
