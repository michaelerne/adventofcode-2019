from functools import partial
from os.path import basename, splitext
from typing import List
from itertools import permutations

from lib import solve
from util import intcode

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)


def thruster_amp(program: List[int], phase_settings: List[int]) -> int:
    _, outputs, _, _, _ = intcode(program.copy(), [phase_settings[0], 0])
    _, outputs, _, _, _ = intcode(program.copy(), [phase_settings[1], outputs[0]])
    _, outputs, _, _, _ = intcode(program.copy(), [phase_settings[2], outputs[0]])
    _, outputs, _, _, _ = intcode(program.copy(), [phase_settings[3], outputs[0]])
    _, outputs, _, _, _ = intcode(program.copy(), [phase_settings[4], outputs[0]])

    return outputs[0]


def thruster_amp_feedback(program: List[int], phase_settings: List[int]) -> int:
    outputs: List[int] = []
    programs: List[List[int]] = [program.copy() for _ in range(0, 5)]
    instruction_pointers = [0 for _ in range(0, 5)]
    inputs = [[x] for x in phase_settings]

    inputs[0].append(0)
    halt_detected = False
    current_program = 0

    while not halt_detected:

        next_program = (current_program + 1) % 5

        _, outputs, programs[current_program], instruction_pointers[current_program], is_halt = intcode(
            programs[current_program],
            inputs[current_program],
            instruction_pointers[current_program]
        )

        # remove the consumed inputs
        inputs[current_program] = []

        # propagate the output to the next amp
        inputs[next_program].append(outputs[0])

        # if the last amp quit with opcode 99
        if current_program == 4 and is_halt:
            halt_detected = True

        current_program = next_program

    return outputs[0]


def part_a(data: List[int]) -> int:
    phase_settings = permutations([0, 1, 2, 3, 4])

    return max(thruster_amp(data, list(x)) for x in phase_settings)


def part_b(data: List[int]) -> int:
    assert thruster_amp_feedback(
        [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0,
         5],
        [9, 8, 7, 6, 5]) == 139629729
    assert thruster_amp_feedback(
        [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1,
         53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0,
         0, 10], [9, 7, 8, 5, 6]) == 18216

    phase_settings = permutations([5, 6, 7, 8, 9])

    return max(thruster_amp_feedback(data, list(x)) for x in phase_settings)


def parse(data: str) -> List[int]:
    return [int(x) for x in data.split(',')]


if __name__ == "__main__":
    SOLVE(part_a, parse, False)

    SOLVE(part_b, parse, False)
