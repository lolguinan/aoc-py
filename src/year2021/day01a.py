#!/usr/bin/env python3

import os


def parse_input(content):
    # Interestingly, off by one when not using ints...
    return list(map(int, filter(None, map(str.strip,
        content.split(os.linesep)))))


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
    increases = count_depth_increases(depths)
    print(increases)


if __name__ == '__main__':
    main()
