"""
Advent of Code Puzzle
"""

from functools import partial
from os.path import basename, splitext
from typing import List

from lib import solve

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)


def fuel(weight: int) -> int:
    return weight // 3 - 2


def part_a(data: List[int]) -> int:
    return sum([fuel(module) for module in data])


def fuel_rec(weight: int) -> int:
    additional_fuel = fuel(weight)
    if additional_fuel <= 0:
        return 0
    return additional_fuel + fuel_rec(additional_fuel)


def part_b(data: List[int]) -> int:
    return sum([fuel_rec(module) for module in data])


def parse(data: str) -> List[int]:
    return [int(x) for x in data.split('\n')]


if __name__ == "__main__":
    SOLVE(part_a, parse)

    SOLVE(part_b, parse)
