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


def has_won(board: list[list[int]], called_numbers: list[int]) -> bool:
    for row in board:
        if not set(row).difference(called_numbers):
            return True
    for index in range(len(board[0])):
        col = [row[index] for row in board]
        if not set(col).difference(called_numbers):
            return True
    return False


def get_score(board: list[list[int]], called_numbers: list[int]) -> int:
    unmarked_sum = 0
    for row in board:
        for col in row:
            if col not in called_numbers:
                unmarked_sum += col
    return unmarked_sum * called_numbers[-1]


def solve(boards: list[list[int]], numbers_to_call: list[int]) -> int:
    # At what number_to_call index does a board win?
    winners = {}

    for board_index, board in enumerate(boards):
        for call_index in range(len(numbers_to_call)):
            called_numbers = numbers_to_call[: call_index + 1]
            if has_won(board, called_numbers):
                winners.setdefault(call_index, []).append(board_index)
                break

    last_call_index = max(winners.keys())
    last_winner = winners[last_call_index][-1]
    last_winner = boards[last_winner]

    return get_score(last_winner, numbers_to_call[: last_call_index + 1])


def main(runner=False):
    with open("inputs/year2021/004.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(*data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
