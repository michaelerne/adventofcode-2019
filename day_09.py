from functools import partial
from os.path import basename, splitext
from typing import List
from queue import SimpleQueue as Queue

from lib import solve
from intcode import IntCode

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)


def part_a(data: List[int]) -> int:
    # test quine
    quine = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    machine = IntCode(quine)
    machine.start()
    machine.join()
    outputs = []
    while machine.output_queue.qsize() > 0:
        outputs.append(machine.output_queue.get())
    assert outputs == quine

    machine = IntCode([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    machine.start()
    machine.join()
    assert len(str(machine.output_queue.get())) == 16

    machine = IntCode([104, 1125899906842624, 99])
    machine.start()
    machine.join()
    assert machine.output_queue.get() == 1125899906842624

    input_queue = Queue()
    input_queue.put(1)
    machine = IntCode(data, input_queue=input_queue)
    machine.start()
    machine.join()

    return machine.output_queue.get()


def part_b(data: List[int]) -> int:
    input_queue = Queue()
    input_queue.put(2)
    machine = IntCode(data, input_queue=input_queue)
    machine.start()
    machine.join()

    return machine.output_queue.get()


def parse(data: str) -> List[int]:
    return [int(x) for x in data.split(',')]


if __name__ == "__main__":
    SOLVE(part_a, parse, False)

    SOLVE(part_b, parse, False)
