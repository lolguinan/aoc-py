#!/usr/bin/env bash

set -eu
set -o pipefail
set -x

show_help() {
    echo "Usage: $0 day-number-and-part [year]"
    echo "Example: $0 01a"
    echo "Example: $0 01a 2015"
}

if [[ $# -lt 1 ]]
then
    show_help
    exit 1
fi

day_part=$1
year=${2:-$(date +%Y)}

src="src/year${year}/day${day_part}.py"
tests="tests/year${year}/test_day${day_part}.py"

vim -p "$src" "$tests"

