from functools import partial
from os.path import basename, splitext
from typing import List
from itertools import permutations
from queue import SimpleQueue as Queue

from lib import solve
from intcode import Intcode

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)


def thruster_amp(program: List[int], phase_settings: List[int]) -> int:
    queues = [Queue() for _ in range(6)]
    for x in range(5):
        queues[x].put(phase_settings[x])
    queues[0].put(0)

    amps = [Intcode(memory=program[:], input_queue=queues[x], output_queue=queues[x + 1]) for x in range(5)]

    for amp in amps:
        amp.start()

    amps[-1].join()
    output = amps[-1].output_queue.get()
    return output


def thruster_amp_feedback(program: List[int], phase_settings: List[int]) -> int:
    queues = [Queue() for _ in range(5)]
    for x in range(5):
        queues[x].put(phase_settings[x])
    queues[0].put(0)

    amps = [Intcode(memory=program[:], input_queue=queues[x], output_queue=queues[(x + 1) % 5]) for x in range(5)]

    for amp in amps:
        amp.start()

    amps[-1].join()
    output = amps[-1].output_queue.get()
    return output


def part_a(data: List[int]) -> int:
    phase_settings = permutations([0, 1, 2, 3, 4])

    assert thruster_amp([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], [4, 3, 2, 1, 0]) == 43210
    assert thruster_amp([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
                         101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], [0, 1, 2, 3, 4]) == 54321
    assert thruster_amp([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
                         1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0], [1, 0, 4, 3, 2]) == 65210

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
