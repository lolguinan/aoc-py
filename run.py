#!/usr/bin/env python3

import argparse
import cProfile
import collections
import datetime
import importlib
import os
import pstats
import re
import sys
import tempfile
import time
import tracemalloc

import tabulate
import tqdm


RunResult = collections.namedtuple(
    "RunResult",
    [
        "response",
        "duration",
        "memory",
    ],
)


def run_module(module_name: str, rounds=1, memory=False) -> RunResult:
    if memory:
        tracemalloc.start()

    start = time.time()
    for _ in range(rounds):
        mod = importlib.import_module(module_name)
        response = mod.main(runner=True)
    stop = time.time()

    if memory:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tracemalloc.reset_peak()
    else:
        peak = None

    return RunResult(response, stop - start, peak)


def profile_module(module_name: str) -> None:
    mod = importlib.import_module(module_name)
    with cProfile.Profile() as pr:
        mod.main(runner=True)
    pr.dump_stats(os.path.join(tempfile.gettempdir(), f"{module_name}.prof"))
    pr.print_stats(pstats.SortKey.CUMULATIVE)


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

    p.add_argument(
        "--memory",
        action="store_true",
        help="track memory allocations (slower)",
    )

    p.add_argument(
        "--profile", action="store_true", help="run cProfile on module (slower)"
    )

    args = p.parse_args()
    if not ((args.day and args.part) or args.all):
        p.print_help()
        sys.exit(1)

    return args


def main():
    args = parse_args()

    target_modules = {}

    if args.day and args.part:
        year_day_part = (args.year, args.day, args.part)
        module_name = f"year{args.year}.day{args.day:02}{args.part}"
        target_modules[year_day_part] = module_name

    elif args.all:
        name_pattern = r"^day(\d{2})([ab])[.]py$"
        container = os.path.join("src", f"year{args.year}")
        candidates = [
            re.findall(name_pattern, candidate) for candidate in os.listdir(container)
        ]
        candidates = [c[0] for c in candidates if len(c) >= 1]
        candidates = [
            [(args.year, int(day), part), f"year{args.year}.day{day}{part}"]
            for day, part in candidates
        ]
        target_modules.update(dict(sorted(candidates)))

    if args.profile:
        if len(target_modules) > 1:
            raise Exception("Too many modules to profile.")
        for year_day_part in target_modules:
            target_module = target_modules[year_day_part]
            profile_module(target_module)
            return

    headers = ["MODULE", "RESPONSE", "TIME (s)"]
    if args.memory:
        headers.append("MEM (MiB)")

    results = []

    pbar = tqdm.tqdm(target_modules)
    for year_day_part in pbar:
        target_module = target_modules[year_day_part]
        pbar.set_description(target_module)
        result = run_module(target_module, args.rounds, args.memory)
        results.append(
            [
                target_module,
                result.response,
                result.duration / args.rounds,
            ]
        )
        if args.memory:
            results[-1].append(result.memory / 1024 / 1024)

    print()
    print(tabulate.tabulate(results, headers=headers, floatfmt=".4f"))


if __name__ == "__main__":
    main()
