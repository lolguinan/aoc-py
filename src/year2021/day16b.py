#!/usr/bin/env python3

import dataclasses
import functools
import operator
import os


HEX_TO_BIN = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def parse_input(content: str) -> str:
    for row in filter(None, map(str.strip, content.split(os.linesep))):
        return row


def convert_hex_to_bin(h_packet: str) -> str:
    return "".join(HEX_TO_BIN[ch] for ch in h_packet)


@dataclasses.dataclass
class BasePacket:
    version: int
    type_id: int


@dataclasses.dataclass
class LiteralPacket(BasePacket):
    value: int


@dataclasses.dataclass
class ChildOffsetPacket(BasePacket):
    length_type_id: int
    sub_packets_total_length: int
    children: list[BasePacket] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ChildCountPacket(BasePacket):
    length_type_id: int
    number_of_sub_packets: int
    children: list[BasePacket] = dataclasses.field(default_factory=list)


def read_bits(bits: str, pointer: int, offset: int) -> tuple[int, str]:
    return pointer + offset, bits[pointer : pointer + offset]


def read_int(bits: str, pointer: int, offset: int) -> tuple[int, int]:
    p = pointer
    p, value = read_bits(bits, pointer, offset)
    return p, int(value, 2)


def read_header(bits: str, pointer: int) -> tuple[int, BasePacket]:
    p = pointer
    offset = 3
    p, version = read_int(bits, p, offset)
    p, type_id = read_int(bits, p, offset)
    return p, BasePacket(version, type_id)


def read_literal(
    bits: str, pointer: int, base: BasePacket
) -> tuple[int, LiteralPacket]:
    p = pointer
    offset = 5

    groups = []
    while True:
        p, group = read_bits(bits, p, offset)
        prefix, group = group[0], group[1:]
        groups.append(group)
        if prefix == "0":
            break
    value = int("".join(groups), 2)

    return p, LiteralPacket(*dataclasses.astuple(base), value)


def read_child_offset(
    bits: str, pointer: int, base: BasePacket
) -> tuple[int, ChildOffsetPacket]:
    p = pointer
    offset = 15
    p, sub_packets_total_length = read_int(bits, p, offset)

    children = []
    arena_start = p
    while p - arena_start < sub_packets_total_length:
        p, child = read_packet(bits, p)
        children.append(child)

    return p, ChildOffsetPacket(
        *dataclasses.astuple(base),
        0,
        sub_packets_total_length,
        children,
    )


def read_child_count(
    bits: str, pointer: int, base: BasePacket
) -> tuple[int, ChildCountPacket]:
    p = pointer
    offset = 11
    p, number_of_sub_packets = read_int(bits, p, offset)

    children = []
    for index in range(number_of_sub_packets):
        p, child = read_packet(bits, p)
        children.append(child)

    return p, ChildCountPacket(
        *dataclasses.astuple(base),
        1,
        number_of_sub_packets,
        children,
    )


def read_packet(bits: str, pointer: int = 0) -> tuple[int, BasePacket]:
    p = pointer

    # literal
    p, base = read_header(bits, pointer)
    if base.type_id == 4:
        return read_literal(bits, p, base)

    # operators
    p, length_type_id = read_int(bits, p, 1)

    # total length in bits of the sub-packets
    if length_type_id == 0:
        return read_child_offset(bits, p, base)

    # number of sub-packets immediately contained
    if length_type_id == 1:
        return read_child_count(bits, p, base)

    raise Exception("Invalid packet during read.")


def render(packet: BasePacket):
    match packet.type_id:
        case 0:  # sum
            return sum(map(render, packet.children))
        case 1:  # product
            return functools.reduce(operator.mul, map(render, packet.children), 1)
        case 2:  # minimum
            return min(map(render, packet.children))
        case 3:  # maximum
            return max(map(render, packet.children))
        case 4:  # literal
            return packet.value
        case 5:  # greater than
            if len(packet.children) != 2:
                raise Exception("Invalid packet during render.")
            left, right = map(render, packet.children)
            return int(left > right)
        case 6:  # less than
            if len(packet.children) != 2:
                raise Exception("Invalid packet during render.")
            left, right = map(render, packet.children)
            return int(left < right)
        case 7:  # equal to
            if len(packet.children) != 2:
                raise Exception("Invalid packet during render.")
            left, right = map(render, packet.children)
            return int(left == right)
        case _:
            raise Exception(f"Unknown packet type ID: {packet.type_id}")


def solve(data: str) -> int:
    _, packet = read_packet(data)
    return render(packet)


def main(runner=False):
    with open("inputs/016.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    data = convert_hex_to_bin(data)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
