from functools import partial
from os.path import basename, splitext
from typing import List

from lib import solve as solve_

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
solve = partial(solve_, DAY)


def part_a(data: List[int]) -> int:
    return 0


def part_b(data: List[int]) -> int:
    return 0


def parse(data: str) -> List[int]:
    return [int(x) for x in data.split('\n')]


if __name__ == "__main__":

    solve(part_a, parse)

    solve(part_b, parse)

