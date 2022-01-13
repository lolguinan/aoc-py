#!/usr/bin/env python3

import enum
import os
import re


Image = dict[tuple[int, int], str]


class Pixel(str, enum.Enum):
    LIGHT = "#"
    DARK = "."


def parse_input(content: str) -> tuple[str, Image]:
    sections = re.split(r"^\s*$", content.strip(), flags=re.MULTILINE)
    enhancement, image, *_ = sections

    enhancement = "".join(map(str.strip, enhancement.split(os.linesep)))
    if len(enhancement) != 512:
        raise Exception(f"Invalid algorithm length: f{len(enhancement)}")

    image = {
        (x, y): cell
        for y, row in enumerate(map(str.strip, image.split(os.linesep)))
        for x, cell in enumerate(row)
    }

    return enhancement, image


def get_corners(image: Image) -> tuple[tuple[int, int]]:
    min_x = min(x for x, y in image)
    min_y = min(y for x, y in image)
    max_x = max(x for x, y in image)
    max_y = max(y for x, y in image)

    return (min_x, min_y), (max_x, max_y)


def render_image(image: Image, default=Pixel.DARK) -> str:
    (min_x, min_y), (max_x, max_y) = get_corners(image)

    output = []
    for y in range(min_y, max_y + 1):
        output.append([])
        for x in range(min_x, max_x + 1):
            output[-1].append(image.get((x, y), default))

    return os.linesep.join(["".join(row) for row in output])


def get_neighborhood(x: int, y: int) -> list[tuple[int, int]]:
    for dy in range(-1, 1 + 1):
        for dx in range(-1, 1 + 1):
            yield x + dx, y + dy


def crop_image(image: Image, empty: Pixel) -> Image:
    (min_x, min_y), (max_x, max_y) = get_corners(image)

    top = all(image[(x, min_y)] == empty for x in range(min_x, max_x + 1))
    if top:
        for x in range(min_x, max_x + 1):
            del image[(x, min_y)]
        return crop_image(image, empty)

    bottom = all(image[(x, max_y)] == empty for x in range(min_x, max_x + 1))
    if bottom:
        for x in range(min_x, max_x + 1):
            del image[(x, max_y)]
        return crop_image(image, empty)

    left = all(image[(min_x, y)] == empty for y in range(min_y, max_y + 1))
    if left:
        for y in range(min_y, max_y + 1):
            del image[(min_x, y)]
        return crop_image(image, empty)

    right = all(image[(max_x, y)] == empty for y in range(min_y, max_y + 1))
    if right:
        for y in range(min_y, max_y + 1):
            del image[(max_x, y)]
        return crop_image(image, empty)

    return image


def apply_enhancement(enhancement: str, image: Image, default=Pixel.DARK) -> Image:
    (min_x, min_y), (max_x, max_y) = get_corners(image)

    edge_pad = 1

    enhanced = {}
    for y in range(min_y - edge_pad, max_y + edge_pad + 1):
        for x in range(min_x - edge_pad, max_x + edge_pad + 1):
            region = [image.get((nx, ny), default) for nx, ny in get_neighborhood(x, y)]
            binary = "".join(["1" if cell == Pixel.LIGHT else "0" for cell in region])
            lookup = int(binary, 2)
            enhanced[(x, y)] = enhancement[lookup]

    return crop_image(enhanced, empty=default)


def solve(data: tuple[str, Image], rounds: int) -> int:
    enhancement, image = data

    empty = enhancement[0]
    full = enhancement[-1]
    defaults = {
        # Empty groups either stay empty or become full.
        Pixel.DARK: Pixel.DARK if empty == Pixel.DARK else Pixel.LIGHT,
        # Full groups either stay full or become empty.
        Pixel.LIGHT: Pixel.LIGHT if full == Pixel.LIGHT else Pixel.DARK,
    }

    # By definition, the initial infinite state is empty.
    default = Pixel.DARK

    for index in range(rounds):
        image = apply_enhancement(enhancement, image, default)
        # print("Round:", index + 1, "inf:", default)
        # print(render_image(image, default))
        # print()
        default = defaults[default]

    return sum(1 if image[(x, y)] == Pixel.LIGHT else 0 for x, y in image)


def main(runner=False):
    with open("inputs/year2021/020.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data, rounds=2)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
