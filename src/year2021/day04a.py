#!/usr/bin/env python3

import os


def parse_input(content: str) -> tuple[list[int], list[list[list[int]]]]:
    numbers = []
    boards = []
    for line in content.split(os.linesep):
        line = line.strip()
        if not line:
            boards.append([])
            continue
        if "," in line:
            numbers = list(map(int, map(str.strip, line.split(","))))
            continue
        boards[-1].append(list(map(int, map(str.strip, line.split()))))

    boards = list(filter(None, boards))

    return boards, numbers


def render_board(board: list[list[int]], called_numbers: list[int]) -> str:
    padding = max([max(map(len, map(str, row))) for row in board])
    render = []
    for row in board:
        render.append(
            " ".join(
                [
                    f"[{col:{padding}}]"
                    if col in called_numbers
                    else f" {col:{padding}} "
                    for col in row
                ]
            )
        )
    return os.linesep.join(render)


def check_winners(
    boards: list[list[list[int]]], called_numbers: list[int]
) -> int | None:
    for board_index, board in enumerate(boards):
        for row_index, row in enumerate(board):
            if not set(row).difference(called_numbers):
                return board_index
        for col_index in range(len(board[0])):
            col = [row[col_index] for row in board]
            if not set(col).difference(called_numbers):
                return board_index
    return None


def solve(boards: list[list[int]], numbers_to_call: list[int]) -> int:
    for index in range(len(numbers_to_call)):
        called_numbers = numbers_to_call[: index + 1]
        winner = check_winners(boards, called_numbers)
        if winner is None:
            continue
        winner = boards[winner]
        unmarked_sum = 0
        for row in winner:
            for col in row:
                if col not in called_numbers:
                    unmarked_sum += col
        return unmarked_sum * called_numbers[-1]


def main(runner=False):
    with open("inputs/004.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(*data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
