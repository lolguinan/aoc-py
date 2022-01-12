#!/usr/bin/env python3

import functools
import itertools
import os
import re


MIN_SCORE = 21


def parse_input(content: str) -> dict[int, int]:
    return {
        1: int(re.search(r"Player 1 .* (\d+)", content).group(1)),
        2: int(re.search(r"Player 2 .* (\d+)", content).group(1)),
    }


# Cache by positions and scores. Only calculate the results of
# (pos1:4, score1:10, pos2:8, score2:3) once, any future instances of
# these positions and scores will result in the same answers.
@functools.cache
def play_through(
    active_position: int,
    active_score: int,
    inactive_position: int,
    inactive_score: int,
):
    # Track win counts for the results of playing out the game
    # in this particular tree in the universes.
    active_wins = inactive_wins = 0
    # Active player rolls 3*3*3 times, producing (1,1,1), (1,1,2), etc.
    for rolls in itertools.product((1, 2, 3), repeat=3):
        # This position and score is one of the 27 spawned universes.
        this_position = ((active_position - 1 + sum(rolls)) % 10) + 1
        this_score = active_score + this_position
        # Either the active player won in this unverse, or the die is handed to
        # the inactive player and the tree of universes grows.
        if this_score >= MIN_SCORE:
            active_wins += 1
        else:
            # Inactive player becomes active player and takes a turn within
            # this particular universe, spawning more universes branching off
            # of the results.
            i_wins, a_wins = play_through(
                inactive_position,
                inactive_score,
                this_position,
                this_score,
            )
            active_wins += a_wins
            inactive_wins += i_wins
    return active_wins, inactive_wins


def solve(start_positions: dict[int, int]) -> int:
    wins1, wins2 = play_through(
        active_position=start_positions[1],
        active_score=0,
        inactive_position=start_positions[2],
        inactive_score=0,
    )
    # print(play_through.cache_info())  # hits=279771, misses=17680
    return max(wins1, wins2)


def main(runner=False):
    with open("inputs/year2021/021.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
