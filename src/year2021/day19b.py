#!/usr/bin/env python3

from __future__ import annotations
import collections
import dataclasses
import functools
import itertools
import math
import os
import re
import typing as T

import numpy as np


MIN_OVERLAP = 12
# In this input, scanner 18 only had 65 matches: (12,2)-1.
MIN_OVERLAP_COMBO_OFFSET = -1


# https://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
RotationMatrix = tuple[
    tuple[int, int, int],
    tuple[int, int, int],
    tuple[int, int, int],
]
ROTATIONS: list[RotationMatrix] = [
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
    ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
    ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
    ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
    ((0, 0, -1), (1, 0, 0), (0, -1, 0)),
    ((-1, 0, 0), (0, -1, 0), (0, 0, 1)),
    ((-1, 0, 0), (0, 0, -1), (0, -1, 0)),
    ((-1, 0, 0), (0, 1, 0), (0, 0, -1)),
    ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
    ((0, 0, 1), (-1, 0, 0), (0, -1, 0)),
    ((0, -1, 0), (-1, 0, 0), (0, 0, -1)),
    ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
    ((0, 0, -1), (0, 1, 0), (1, 0, 0)),
    ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
    ((0, 0, 1), (0, -1, 0), (1, 0, 0)),
    ((0, -1, 0), (0, 0, -1), (1, 0, 0)),
    ((0, 0, -1), (0, -1, 0), (-1, 0, 0)),
    ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
    ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
    ((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
]


@dataclasses.dataclass(frozen=True, order=True)
class Vector3:
    x: int
    y: int
    z: int

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __repr__(self) -> str:
        return f"V({self.x},{self.y},{self.z})"


@dataclasses.dataclass(frozen=True)
class RT:
    rotation: RotationMatrix
    translation: Vector3


def parse_input(content: str) -> dict[int, set[Vector3]]:
    data = collections.defaultdict(set)
    last_key = None
    for row in filter(None, map(str.strip, content.split(os.linesep))):
        if "---" in row:
            last_key = int(re.findall(r"(\d+)", row)[0])
            continue
        data[last_key].update([Vector3(*map(int, re.findall(r"([-]?\d+)", row)))])
    return data


def get_manhattan_distance(a: Vector3, b: Vector3) -> int:
    x = abs(b.x - a.x)
    y = abs(b.y - a.y)
    z = abs(b.z - a.z)
    return x + y + z


def get_distance_squared(a: Vector3, b: Vector3) -> int:
    x = (b.x - a.x) ** 2
    y = (b.y - a.y) ** 2
    z = (b.z - a.z) ** 2
    return x + y + z


def get_fingerprint(
    beacons: set[Vector3],
) -> dict[int, tuple[Vector3, Vector3]]:
    # Distances between all unique point combinations within this scanner.
    combinations = itertools.combinations(sorted(beacons), 2)
    return {get_distance_squared(a, b): (a, b) for a, b in combinations}


@functools.cache
def get_combination_count(n, r):
    # Number of combinations for n items choose r.
    return math.factorial(n) / math.factorial(r) / math.factorial(n - r)


def get_fingerprint_overlaps(
    scanner_fingerprints: dict[int, set[int]]
) -> set[tuple[int, int]]:
    # Scanner pairs with overlapping distances between beacon pairs.
    overlap_threshold = get_combination_count(MIN_OVERLAP, 2)
    overlap_threshold += MIN_OVERLAP_COMBO_OFFSET
    overlaps = set()
    for s1, s2 in itertools.combinations(scanner_fingerprints, 2):
        f1 = scanner_fingerprints[s1]
        f2 = scanner_fingerprints[s2]
        overlap = set(f1.keys()).intersection(f2.keys())
        if len(overlap) >= overlap_threshold:
            overlaps.add((s1, s2))
    return overlaps


def apply_rotation(r: RotationMatrix, v: Vector3) -> Vector3:
    r = np.array(r)
    a = np.array([[v.x], [v.y], [v.z]])
    ra = np.matmul(r, a)
    return Vector3(*map(int, ra[:, 0]))


def apply_candidate_rotations(
    vs: list[Vector3],
) -> T.Iterable[tuple[RotationMatrix, list[Vector3]]]:
    for rotation in ROTATIONS:
        r = np.array(rotation)
        a = np.array([[[v.x], [v.y], [v.z]] for v in vs])
        ra = np.matmul(r, a)
        yield rotation, [Vector3(*map(int, row[:, 0])) for row in ra]


def merge_intrinsic_rotations(r0: RotationMatrix, r1: RotationMatrix) -> RotationMatrix:
    # Intrinsic matrix multiplication (matrices are not in world perspective)
    # chains are right-to-left, moving r1 into r0's frame. Note that this seems
    # backwards since it's rotating r0 by r1, but it makes the example happy.
    return np.matmul(np.array(r1), np.array(r0)).tolist()


def get_translation(
    s0_beacons: list[Vector3], s1_beacons: list[Vector3]
) -> Vector3 | None:
    # Find a transation (x,y,z) from s1 to s0 (if there is one).
    # Note that this seems backwards, but it makes the example happy.
    # t = a - b => a = t + b => s0 = s1 + t
    #              b = a - t => s1 = s0 - t
    candidates = collections.Counter()
    for a in s0_beacons:
        for b in s1_beacons:
            t = a - b
            candidates[t] += 1
            if candidates[t] >= MIN_OVERLAP:
                return t
    return None


def get_scanner_offset(
    s0_beacons: list[Vector3], s1_beacons: list[Vector3]
) -> RT | None:
    # Find a rotation and translation to move s1 to s0 (if there is one).
    for rotation, s1_rotated in apply_candidate_rotations(s1_beacons):
        t = get_translation(s0_beacons, s1_rotated)
        if t is not None:
            return RT(rotation, t)
    return None


def dfs(
    graph: dict[T.Hashable, T.Hashable],
    node: T.Hashable,
    discovered: set[T.Hashable] = None,
) -> T.Iterator[T.Hashable]:
    if discovered is None:
        discovered = set()
    discovered.add(node)
    yield node
    for child in graph.get(node, []):
        if child not in discovered:
            yield from dfs(graph, child, discovered)


def get_origin_offsets(scanners: dict[int, set[Vector3]]) -> dict[int, RT]:
    # {0: {dist**2: (V3, V3), ...}, ...}
    fingerprints = {scanner: get_fingerprint(scanners[scanner]) for scanner in scanners}

    overlaps = get_fingerprint_overlaps(fingerprints)
    overlaps = collections.defaultdict(list)
    for a, b in get_fingerprint_overlaps(fingerprints):
        overlaps[a].append(b)
        overlaps[b].append(a)

    unmatched = set(overlaps)
    unmatched |= set(list(itertools.chain.from_iterable(overlaps.values())))
    unmatched = set(scanners) - unmatched
    if unmatched:
        unmatched = ",".join(map(str, sorted(unmatched)))
        raise Exception(f"Unmatched scanners: {unmatched}")

    accumulator: dict[int, RT] = {}
    lineage: dict[int, int] = {}
    for parent in dfs(overlaps, 0):
        if not accumulator:
            accumulator[parent] = RT(None, Vector3(0, 0, 0))
            lineage[parent] = None
        for child in sorted(overlaps[parent]):
            if child in accumulator:
                continue
            offset = get_scanner_offset(scanners[parent], scanners[child])
            if offset is None:
                raise Exception(f"No overlaps for {parent} and {child}.")
            accumulator[child] = offset
            lineage[child] = parent

    for a, b in lineage.items():
        if lineage.get(b) == a:
            raise Exception(f"Cycle in lineage: {a} begets {b} begets {a}.")

    offsets = {}
    for child in lineage:
        crt = accumulator[child]
        r = crt.rotation
        t = crt.translation
        parent = lineage[child]
        while parent is not None and accumulator[parent].rotation is not None:
            prt = accumulator[parent]
            r = merge_intrinsic_rotations(r, prt.rotation)
            t = apply_rotation(prt.rotation, t)
            t += prt.translation
            parent = lineage[parent]
        offsets[child] = RT(r, t)

    return offsets


def merge_scanners(
    scanners: dict[int, set[Vector3]], offsets: dict[int, RT]
) -> set[Vector3]:
    unique = set()
    for scanner, beacons in scanners.items():
        rt = offsets[scanner]
        if rt.rotation is None:
            unique |= beacons
        else:
            rotated = [apply_rotation(rt.rotation, v) for v in beacons]
            # t = a - b => a = t + b => s0 = s1 + t
            #              b = a - t => s1 = s0 - t
            translated = [v + rt.translation for v in rotated]
            unique |= set(translated)
    return unique


def solve(data: dict[int, set[Vector3]]) -> int:
    offsets = get_origin_offsets(data)
    distances = {
        (a, b): get_manhattan_distance(
            offsets[a].translation,
            offsets[b].translation,
        )
        for a, b in itertools.combinations(offsets, 2)
    }
    for distance in sorted(distances.values(), reverse=True):
        return distance


def main(runner=False):
    with open("inputs/year2021/019.txt") as fp:
        content = fp.read()

    data = parse_input(content)
    answer = solve(data)
    if runner:
        return answer
    print(answer)


if __name__ == "__main__":
    main()
