#!/usr/bin/env python3

import argparse
import datetime
import importlib
import os
import re
import sys
import time

import tabulate


def first_or_default(seq, default=None):
    try:
        return next(iter(seq))
    except StopIteration:
        return default


def run_module(module_name, rounds=1):
    start = time.time()
    for _ in range(rounds):
        mod = importlib.import_module(module_name)
        response = mod.main(runner=True)
    stop = time.time()
    return response, stop - start


def parse_args():
    p = argparse.ArgumentParser()
    p.description = "Solution runner."

    p.add_argument(
        "-y",
        "--year",
        type=int,
        default=datetime.datetime.now().year,
        help="year number (example: 2015)",
    )

    p.add_argument("-d", "--day", type=int, help="day number (example: 1)")

    p.add_argument("-p", "--part", choices=["a", "b"], help="part letter (example: a)")

    p.add_argument("-a", "--all", action="store_true", help="run everything")

    p.add_argument(
        "--rounds",
        metavar="N",
        type=int,
        default=1,
        help="number of times to run each solution",
    )

    args = p.parse_args()
    if not ((args.day and args.part) or args.all):
        p.print_help()
        sys.exit(1)

    return args


def main():
    args = parse_args()

    target_modules = []

    if args.day and args.part:
        module_name = f"year{args.year}.day{args.day:02}{args.part}"
        target_modules.append(module_name)

    elif args.all:
        name_pattern = r"^(day\d{2}[ab])[.]py$"
        container = os.path.join("src", f"year{args.year}")
        target_modules.extend(
            sorted(
                f"year{args.year}.{candidate}"
                for candidate in filter(
                    None,
                    [
                        first_or_default(re.findall(name_pattern, candidate))
                        for candidate in os.listdir(container)
                    ],
                )
            )
        )

    results = []
    print("Working", end="", flush=True)
    for target_module in target_modules:
        response, duration = run_module(target_module, args.rounds)
        results.append([target_module, response, duration / args.rounds])
        print(".", end="", flush=True)
    print()
    print()

    print(
        tabulate.tabulate(
            results, headers=["MODULE", "RESPONSE", "DURATION"], floatfmt=".4f"
        )
    )


if __name__ == "__main__":
    main()
