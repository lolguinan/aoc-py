#!/usr/bin/env python3

import os
import re


def parse_input(content: str) -> dict[int, int]:
    return {
        1: int(re.search(r"Player 1 .* (\d+)", content).group(1)),
        2: int(re.search(r"Player 2 .* (\d+)", content).group(1)),
    }


class BaseDie:
    def __init__(self, sides: int):
        self.sides = sides
        self.rolled = 0

    def roll(self):
        raise NotImplemented()


class DeterministicDie(BaseDie):
    def __init__(self, sides: int):
        super().__init__(sides)
        self.current = -1

    def roll(self):
        self.rolled += 1
        self.current = (self.current + 1) % self.sides
        return self.current + 1


def play_round(
    min_score: int, positions: dict[int, int], scores: dict[int, int], die: BaseDie
) -> tuple[dict[int, int], dict[int, int]]:

    for player in sorted(positions):
        advance = sum(die.roll() for _ in range(3))
        positions[player] = ((positions[player] - 1 + advance) % 10) + 1
        scores[player] += positions[player]
        if scores[player] >= min_score:
            break

    return positions, scores


def play_until(
    min_score: int, start_positions: dict[int, int], die: BaseDie
) -> tuple[int, dict[int, int], dict[int, int], BaseDie]:

    positions = {player: pos for player, pos in start_positions.items()}
    scores = {player: 0 for player in start_positions}

    turns = 0
    while True:
        positions, scores = play_round(min_score, positions, scores, die)
        if any(score >= min_score for score in scores.values()):
            break

    return turns, positions, scores, die


def solve(min_score: int, start_positions: dict[int, int]) -> int:
    die = DeterministicDie(100)
    turns, positions, scores, die = play_until(min_score, start_positions, die)
    losing_score = min(scores[1], scores[2])
    return losing_score * die.rolled


def main(runner=False):
    with open("inputs/year2021/021.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(1000, data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
