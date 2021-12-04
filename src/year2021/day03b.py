#!/usr/bin/env python3

import collections
import enum
import os


def parse_input(content) -> list[list[int]]:
    return [
        list(map(int, list(row)))
        for row in filter(None, map(str.strip,
            content.split(os.linesep)))
    ]


def bit_row_to_decimal(row: list[int]) -> int:
    return int(''.join(map(str, row)), 2)


class Commonality(enum.Enum):
    LEAST = 0
    MOST = 1


def bit_criteria(data: list[list[int]], commonality) -> list[int]:
    index = 0
    while index < len(data[0]) and len(data) > 1:
        counts = collections.Counter([
            row[index] for row in data
        ])
        (most_bit, most_count), (least_bit, least_count) = counts.most_common()
        if most_count == least_count:
            discriminator = commonality.value
        else:
            match commonality:
                case Commonality.LEAST:
                    discriminator = least_bit
                case Commonality.MOST:
                    discriminator = most_bit
                case _:
                    raise Exception(f'Unknown commonality: {commonality}')
        data = [
            row for row in data
            if row[index] == discriminator
        ]
        index += 1
    return data[0]


def get_life_support(data: list[list[int]]) -> int:
    oxygen_generator = bit_criteria(data, Commonality.MOST)
    oxygen_generator = bit_row_to_decimal(oxygen_generator)
    co2_scrubber = bit_criteria(data, Commonality.LEAST)
    co2_scrubber = bit_row_to_decimal(co2_scrubber)

    return oxygen_generator * co2_scrubber


def solve(data: list[list[int]]) -> int:
    return get_life_support(data)


def main():
    with open('inputs/003.txt') as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    print(answer)


if __name__ == '__main__':
    main()
