#!/usr/bin/env python3

# Similar 3x5 figlet font: http://www.figlet.org/fontdb_example.cgi?font=3x5.flf

# https://www.reddit.com/r/adventofcode/comments/rfday0/2021_day_13_part_2_need_letters/
# https://github.com/mstksg/advent-of-code-ocr/blob/main/src/Advent/OCR/LetterMap.hs

import os


V2 = tuple[int, int]


def _to_matrix(embed: str, pixel: str = "#") -> list[list[str]]:
    matrix = list(map(list, filter(None, map(str.strip, embed.split(os.linesep)))))
    if not matrix:
        raise Exception("No matrix generated. Empty embed?")
    if len(set(map(len, matrix))) != 1:
        raise Exception("Irregular matrix generated.")
    return matrix


def _make_x_partition(
    x0: int, y0: int, x1: int, y1: int, at_x: int
) -> list[V2, V2, V2, V2]:
    if not x0 < at_x < x1:
        raise Exception("Partition at_x must be within (x0, x1).")
    return [
        (x0, y0),
        (at_x - 1, y1),
        (at_x + 1, y0),
        (x1, y1),
    ]


def _find_letters(embed: str, pixel: str = "#") -> list[list[list[str]]]:
    matrix = _to_matrix(embed, pixel)
    height = len(matrix)
    width = len(matrix[0])

    column_dividers = []
    for x in range(width):
        column = [matrix[y][x] for y in range(height)]
        if all(cell != pixel for cell in column):
            column_dividers.append(x)

    letter_areas = []
    x0, y0, x1, y1 = 0, 0, width - 1, height - 1
    for column_divider in column_dividers:
        partition = _make_x_partition(x0, y0, x1, y1, column_divider)
        (nx0, ny0), (nx1, ny1), (x0, y0), (x1, y1) = partition
        letter_areas.append([(nx0, ny0), (nx1, ny1)])
    letter_areas.append([(x0, y0), (x1, y1)])

    letters = []
    for (x0, y0), (x1, y1) in letter_areas:
        letters.append(
            [[matrix[y][x] for x in range(x0, x1 + 1)] for y in range(y0, y1 + 1)]
        )

    return letters


_RAW_LETTERS = "ABCEFGHJKLPRUZ"

_RAW_LETTERS_EMBED = """
.##. ###. .##. #### #### .##. #..# ..## #..# #... ###. ###. #..# ####
#..# #..# #..# #... #... #..# #..# ...# #.#. #... #..# #..# #..# ...#
#..# ###. #... ###. ###. #... #### ...# ##.. #... #..# #..# #..# ..#.
#### #..# #... #... #... #.## #..# ...# #.#. #... ###. ###. #..# .#..
#..# #..# #..# #... #... #..# #..# #..# #.#. #... #... #.#. #..# #...
#..# ###. .##. #### #... .### #..# .##. #..# #### #... #..# .##. ####
""".strip()

LETTERS = dict(
    (letter, found)
    for letter, found in zip(_RAW_LETTERS, _find_letters(_RAW_LETTERS_EMBED))
)


def _translate_letter(found: list[list[str]], pixel: str = "#") -> str:
    for letter, exploded in LETTERS.items():
        if exploded == found:
            return letter
    raise Exception("Letter not translated.")


def translate(embed_for_ocr: str, pixel: str = "#") -> str:
    letters = _find_letters(embed_for_ocr, pixel)
    return "".join([_translate_letter(letter, pixel) for letter in letters])
