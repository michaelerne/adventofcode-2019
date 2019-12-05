from functools import partial
from os.path import basename, splitext
from typing import List

from lib import solve
from util import intcode


DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)


def part_a(data: List[int]) -> int:
    _, outputs = intcode(data, [1])
    return outputs[-1]


def part_b(data: List[int]) -> int:
    _, outputs = intcode(data, [5])
    return outputs[-1]


def parse(data: str) -> List[int]:
    return [int(x) for x in data.split(',')]


if __name__ == "__main__":

    SOLVE(part_a, parse, False)

    SOLVE(part_b, parse, False)
