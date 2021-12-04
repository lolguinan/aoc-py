#!/usr/bin/env bash

show_help() {
    echo "Usage: $0 day-number-and-part"
    echo "Example: $0 01a"
}

if [[ $# -lt 1 ]]
then
    show_help
    exit 1
fi

src="src/year2021/day$1.py"
tests="tests/test_day$1.py"

vim -p "$src" "$tests"

