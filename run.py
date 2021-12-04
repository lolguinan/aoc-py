#!/usr/bin/env python3

import argparse
import importlib
import os
import re
import time


def first_or_default(seq, default=None):
    try:
        return next(iter(seq))
    except StopIteration:
        return default


def run_module(module_name):
    print('Module:', module_name)
    start = time.time()
    mod = importlib.import_module(module_name)
    mod.main()
    stop = time.time()
    print(f'Runtime: {stop - start:.19f}')


def parse_args():
    p = argparse.ArgumentParser()
    p.description = 'Solution runner.'

    p.add_argument('-d', '--day',
        type=int,
        help='day number (example: 1)')

    p.add_argument('-p', '--part',
        choices=['a', 'b'],
        help='part letter (example: a)')

    p.add_argument('-a', '--all',
        action='store_true',
        help='run everything')

    return p.parse_args()


def main():
    args = parse_args()
    if args.day and args.part:
        module_name = f'year2021.day{args.day:02}{args.part}'
        run_module(module_name)
        return

    if args.all:
        name_pattern = r'^(day\d{2}[ab])[.]py$'
        container = os.path.join('src', 'year2021')
        candidates = sorted(filter(None, [
            first_or_default(re.findall(name_pattern, candidate))
            for candidate in os.listdir(container)
        ]))
        for candidate in candidates:
            module_name = f'year2021.{candidate}'
            run_module(module_name)
            print()


if __name__ == '__main__':
    main()
