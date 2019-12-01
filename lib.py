import os
from typing import Callable, List, Union, Tuple, Any

import requests
from aocd import data, submit  # type: ignore
from aocd.models import Puzzle  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

# type definitions
AOC_INPUT = str
INPUT = Union[int, str]
OUTPUT = int

FN = Callable[[List[INPUT]], OUTPUT]
PARSE_FN = Callable[[AOC_INPUT], List[INPUT]]
TEST_CASE = Tuple[INPUT, OUTPUT]

default_parser: Callable[[Any], Any] = lambda x: x


def parse_int_if_possible(input: str) -> Union[str, int]:
    try:
        return int(input)
    except ValueError:
        return input


def get_test_cases(day: int, part_input: str) -> List[TEST_CASE]:
    test_cases = []

    resp = requests.get(f"https://adventofcode.com/2019/day/{day}",
                        cookies={"session": os.getenv("AOC_SESSION")},
                        headers={"User-Agent": "michaelerne 0.0.1"}
                        )
    html = BeautifulSoup(resp.content, features='html.parser')

    # parts are <article class="day-desc">
    parts = html.body.find_all('article', attrs={'class': 'day-desc'})
    if part_input == 'a':
        part = parts[0]
    else:
        part = parts[1]

    # each part has a <ul>
    ul = part.find('ul')

    # each <li> within that <ul> is a test case
    lis = ul.find_all('li')

    for li in lis:
        # each <li> has multiple <code> segments
        codes = li.find_all('code')

        # assume that the first <code> is input
        input = codes[0].text

        # assume that the last <code> contains expected_output
        output = codes[-1].text

        # if there is a =, the expected output is at the very end
        if '=' in output:
            output = output.split(' = ')[-1]

        # if they can be ints, let them be ints
        input = parse_int_if_possible(input)
        output = parse_int_if_possible(output)

        test_cases.append((input, output))

    return test_cases


def solve(day: int, fn: FN, parse_fn: PARSE_FN = default_parser, test_cases: List[TEST_CASE] = None):
    part = fn.__name__.split('_')[1]

    if not test_cases:
        print(f"# TEST CASES")
        test_cases = get_test_cases(day, part)
        if len(test_cases) > 0:
            print(f"OK: generated [{len(test_cases)}] test cases")
        else:
            print(f"FAIL: generated [{len(test_cases)} test cases")

    print("# TESTS")
    fails = 0
    for input, expected_output in test_cases:
        actual_output = fn([input])
        if actual_output != expected_output:
            print(f"FAIL: input [{input}] -> actual [{actual_output}] != expected [{expected_output}]")
            fails += 1
        else:
            print(f"OK: input [{input}] -> actual [{actual_output}] == expected [{expected_output}]")

    if fails > 0:
        print(f"ABORT: encountered {fails} failures in test_cases!")
        return

    print(f"# PARSING")
    parsed_data = parse_fn(data)

    print(f"# SOLVING")
    answer = fn(parsed_data)
    print(f"SOLVED: answer [{answer}]")

    print(f"# VERIFICATION")
    # see if we already solved it
    puzzle = Puzzle(year=2019, day=day)
    try:
        if part == 'a':
            correct_answer = puzzle.answer_a
        else:
            correct_answer = puzzle.answer_b
    except AttributeError:
        # we did not solve it yet
        print(f"SUBMIT: answer [{answer}]")
        resp = submit(answer, part=part, day=day, year=2019)
        if resp.status_code == 200:
            return True
        else:
            return False

    # we solved it already
    print(f"ALREADY SOLVED: correct_answer [{correct_answer}]")
    if str(answer) == correct_answer:
        print(f"OK: answer [{answer}]")
    else:
        print(f"FAIL: answer [{answer}] != correct_answer [{correct_answer}]")
