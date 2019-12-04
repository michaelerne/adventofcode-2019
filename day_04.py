from functools import partial
from os.path import basename, splitext
from typing import List, Tuple
from collections import Counter

# pylint: disable=W0611
import multiprocessing

from lib import solve

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)

Password = List[int]
Digits = List[int]


def has_pairs(digits: Digits) -> bool:
    return any(x >= 2 for x in Counter(digits).values())


def has_no_uneven_groups(digits: Digits) -> bool:
    return any(x == 2 for x in Counter(digits).values())


def never_decreases(digits: Digits) -> bool:
    return digits == sorted(digits)


def is_valid_a(number: int) -> bool:
    digits = [int(x) for x in str(number)]

    if has_pairs(digits) and never_decreases(digits):
        return True

    return False


def is_valid_a_as_int(number: int) -> int:
    if is_valid_a(number):
        return 1
    return 0


def part_a(data: List[int]) -> int:
    range_from, range_to = data

    # single core
    number_that_are_valid = sum(1 for x in range(range_from, range_to + 1) if is_valid_a(x))

    # multi core
    # pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    # number_that_are_valid = sum(pool.map(is_valid_a_as_int, range(range_from, range_to + 1)))

    return number_that_are_valid


def is_valid_b(number: int) -> bool:
    digits = [int(x) for x in str(number)]

    if has_no_uneven_groups(digits) and never_decreases(digits):
        return True

    return False


def is_valid_b_as_int(number: int) -> int:
    if is_valid_b(number):
        return 1
    return 0


def part_b(data: List[int]) -> int:
    range_from, range_to = data

    # single core
    number_that_are_valid = sum(1 for x in range(range_from, range_to + 1) if is_valid_b(x))

    # multi core
    # pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    # number_that_are_valid = sum(pool.map(is_valid_b_as_int, range(range_from, range_to + 1)))

    return number_that_are_valid


def parse(data: str) -> Tuple[int, int]:
    left, right = [int(x) for x in data.split('-')]

    return left, right


if __name__ == "__main__":

    SOLVE(part_a, parse, False, [('111111-111111', 1),
                                 ('223450-223450', 0),
                                 ('123789-123789', 0)])

    SOLVE(part_b, parse, False, [('112233-112233', 1),
                                 ('123444-123444', 0),
                                 ('111122-111122', 1)])
