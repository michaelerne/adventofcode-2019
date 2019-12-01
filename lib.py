"""
Misc functions
"""
import os
from typing import Callable, List, Union, Tuple, Any

import requests
# pylint: disable=E0611
# pylint does not like the way aocd exposes data. I don't care.
from aocd import data, submit  # type: ignore
from aocd.models import Puzzle  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

# type definitions
AOCInput = str
Input = Union[int, str]
Output = int

Function = Callable[[List[Input]], Output]
ParseFunction = Callable[[AOCInput], List[Input]]
TestCase = Tuple[Input, Output]

default_parser: Callable[[Any], Any] = lambda x: x


def parse_int_if_possible(possible_int: str) -> Union[str, int]:
    """
    Parses the parameter to int if possible
    """
    try:
        return int(possible_int)
    except ValueError:
        return possible_int


def get_test_cases(day: int, part_input: str) -> List[TestCase]:
    """
    Retrieves the test cases from adventofcode.com
    """
    test_cases = []

    resp = requests.get(f"https://adventofcode.com/2019/day/{day}",
                        cookies={"session": os.getenv("AOC_SESSION")},
                        headers={"User-Agent": "michaelerne 0.0.1"}
                        )
    html = BeautifulSoup(resp.content, features='html.parser')

    # parts are <article class="day-desc">
    parts_html = html.body.find_all('article', attrs={'class': 'day-desc'})
    if part_input == 'a':
        part_html = parts_html[0]
    else:
        part_html = parts_html[1]

    # each part has a <ul>
    ul_html = part_html.find('ul')

    # each <li> within that <ul> is a test case
    lis_html = ul_html.find_all('li')

    for li_html in lis_html:
        # each <li> has multiple <code> segments
        codes_html = li_html.find_all('code')

        # assume that the first <code> is input
        puzzle_input = codes_html[0].text

        # assume that the last <code> contains expected_output
        output = codes_html[-1].text

        # if there is a =, the expected output is at the very end
        if '=' in output:
            output = output.split(' = ')[-1]

        # if they can be ints, let them be ints
        puzzle_input = parse_int_if_possible(puzzle_input)
        output = parse_int_if_possible(output)

        test_cases.append((puzzle_input, output))

    return test_cases


# pylint: disable=R0912
# pylint does not like to many branches. I don't care.
def solve(day: int,
          function: Function,
          parse_function: ParseFunction = default_parser,
          test_cases: List[TestCase] = None):
    """
    Solves a puzzle
    """
    part = function.__name__.split('_')[1]

    if not test_cases:
        print(f"# TEST CASES")
        test_cases = get_test_cases(day, part)
        if len(test_cases) > 0:
            print(f"OK: generated [{len(test_cases)}] test cases")
        else:
            print(f"FAIL: generated [{len(test_cases)} test cases")

    print("# TESTS")
    fails = 0
    for puzzle_input, expected_output in test_cases:
        actual_output = function([puzzle_input])
        if actual_output != expected_output:
            print(f"FAIL: input [{puzzle_input}] -> actual [{actual_output}] "
                  f"!= expected [{expected_output}]")
            fails += 1
        else:
            print(f"OK: input [{puzzle_input}] -> actual [{actual_output}] "
                  f"== expected [{expected_output}]")

    if fails > 0:
        print(f"ABORT: encountered {fails} failures in test_cases!")
        return False

    print(f"# PARSING")
    parsed_data = parse_function(data)

    print(f"# SOLVING")
    answer = function(parsed_data)
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
        return False

    # we solved it already
    print(f"ALREADY SOLVED: correct_answer [{correct_answer}]")
    if str(answer) == correct_answer:
        print(f"OK: answer [{answer}]")
    else:
        print(f"FAIL: answer [{answer}] != correct_answer [{correct_answer}]")

    return True
