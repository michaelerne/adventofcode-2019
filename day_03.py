from functools import partial
from os.path import basename, splitext
from typing import List, Tuple, Set
import sys

from lib import solve

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)

Coordinate = Tuple[int, int]
Wire = List[Coordinate]


def part_a(data: List[Wire]) -> int:
    wire_a: Wire = data[0]
    wire_b: Wire = data[1]

    crossings: Set[Coordinate] = set(wire_a).intersection(wire_b)

    distances: List[int] = [abs(x) + abs(y) for x, y in crossings if x + y != 0]

    return min(distances)


def part_b(data: List[Wire]) -> int:
    wire_a: Wire = data[0]
    wire_b: Wire = data[1]

    crossings = set(wire_a).intersection(wire_b)

    steps_to_crossing = [wire_a.index(crossing) + wire_b.index(crossing)
                         for crossing in crossings if crossing != (0, 0)]

    return min(steps_to_crossing)


def parse(data: str) -> List[Wire]:
    wires_raw = data.split('\n')
    wires = []

    for wire_raw in wires_raw:

        direction_changes: List[str] = wire_raw.split(',')

        x_coord = 0
        y_coord = 0

        path = [(0, 0)]

        for direction_change in direction_changes:
            direction = direction_change[0]
            movement_amount = int(direction_change[1:])

            if direction == 'R':
                x_change = 1
                y_change = 0
            elif direction == 'L':
                x_change = -1
                y_change = 0
            elif direction == 'U':
                x_change = 0
                y_change = 1
            elif direction == 'D':
                x_change = 0
                y_change = -1
            else:
                sys.exit(0)

            for _ in range(0, movement_amount):
                x_coord += x_change
                y_coord += y_change
                path.append((x_coord, y_coord))

        wires.append(path)

    return wires


if __name__ == "__main__":
    SOLVE(part_a, parse, True, [('R8,U5,L5,D3\nU7,R6,D4,L4', 6)])

    SOLVE(part_b, parse, True, [('R8,U5,L5,D3\nU7,R6,D4,L4', 30)])
