#!/usr/bin/env python3

import argparse
import datetime
import os
import shutil


START_IN = os.path.dirname(os.path.realpath(__file__))


def resolve_paths(year: int, day: int) -> dict:
    def make_rel_path(filepath):
        return os.path.relpath(os.path.realpath(filepath))

    day = f"{day:02}"
    src = os.path.join(START_IN, "..", "src", f"year{year}")
    tests = os.path.join(START_IN, "..", "tests", f"year{year}")
    return {
        "src": {
            "a": make_rel_path(os.path.join(src, f"day{day}a.py")),
            "b": make_rel_path(os.path.join(src, f"day{day}b.py")),
        },
        "tests": {
            "a": make_rel_path(os.path.join(tests, f"test_day{day}a.py")),
            "b": make_rel_path(os.path.join(tests, f"test_day{day}b.py")),
        },
    }


def check_paths(paths: dict):
    errors = []
    for kind in paths:
        for part in paths[kind]:
            filepath = paths[kind][part]
            if part == "a":
                if not os.path.exists(filepath):
                    errors.append(f"Source does not exist: {filepath}")
            elif part == "b":
                if os.path.exists(filepath):
                    errors.append(f"Destination already exists: {filepath}")
            else:
                raise Exception(f"Unknown path part: {part}")
    return errors


def parse_args():
    p = argparse.ArgumentParser()
    p.description = "Copy some day A files to day B files."

    p.add_argument(
        "-y",
        "--year",
        type=int,
        default=datetime.datetime.now().year,
        help="year number (example: 2015)",
    )

    p.add_argument("day", type=int, help="day number")

    p.add_argument("-d", "--dry", action="store_true", help="show what would happen")

    return p.parse_args()


def main():
    args = parse_args()

    paths = resolve_paths(args.year, args.day)
    errors = check_paths(paths)

    if args.dry:
        if errors:
            print("Errors:")
            print(os.linesep.join(errors))
        for kind in paths:
            print("Copy:")
            print("SRC:", paths[kind]["a"])
            print("DST:", paths[kind]["b"])
        return

    if errors:
        raise Exception(os.linesep.join(errors))

    for kind in paths:
        shutil.copy2(paths[kind]["a"], paths[kind]["b"])


if __name__ == "__main__":
    main()
