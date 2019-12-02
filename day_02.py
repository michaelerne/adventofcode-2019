from functools import partial
from os.path import basename, splitext
from typing import List

from lib import solve
from util import intcode

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)


def part_a(data: List[int]) -> int:
    # modify
    data[1] = 12
    data[2] = 2

    return intcode(data)


def part_b(data: List[int]) -> int:
    goal = 19690720

    for noun in range(0, 99):
        for verb in range(0, 99):

            test_data = data.copy()

            # modify
            test_data[1] = noun
            test_data[2] = verb

            answer = intcode(test_data)
            if answer == goal:
                return 100 * noun + verb
    print('WHOOPS')
    return -1


def parse(data: str) -> List[int]:
    return [int(x) for x in data.split(',')]


if __name__ == "__main__":

    # test generation does not work, skipping tests in favor of doctests in utils.py

    SOLVE(part_a, parse, False, [])

    SOLVE(part_b, parse, False, [])