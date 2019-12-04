import sys
from functools import partial
from os.path import basename, splitext
from typing import List, Set, Tuple

from lib import solve

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)

Coordinate = int
CoordinatePair = Tuple[Coordinate, Coordinate]
Direction = str
MovementAmount = int
DirectionChange = str
Wire = List[CoordinatePair]


def part_a(data: List[Wire]) -> int:
    wire_a: Wire = data[0]
    wire_b: Wire = data[1]

    crossings: Set[CoordinatePair] = set(wire_a).intersection(wire_b)

    distances: List[int] = [abs(x) + abs(y) for x, y in crossings if not (x == 0 and y == 0)]

    return min(distances)


def part_b(data: List[Wire]) -> int:
    wire_a: Wire = data[0]
    wire_b: Wire = data[1]

    crossings = set(wire_a).intersection(wire_b)

    steps_to_crossing = [wire_a.index(crossing) + wire_b.index(crossing)
                         for crossing in crossings if crossing != (0, 0)]

    return min(steps_to_crossing)


def get_coordinate_change_for_direction(direction: Direction) -> CoordinatePair:
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
        print(f"found unknown direction: [{direction}]")
        sys.exit(0)

    return x_change, y_change


def process(wire: Wire,
            direction_changes: List[DirectionChange],
            x_coord: Coordinate,
            y_coord: Coordinate) -> Wire:

    if len(direction_changes) == 0:
        return wire

    direction_change: DirectionChange = direction_changes[0]
    remaining_direction_changes: List[DirectionChange] = direction_changes[1:]

    direction: Direction = direction_change[0]
    movement_amount: MovementAmount = int(direction_change[1:])

    x_change, y_change = get_coordinate_change_for_direction(direction)

    for _ in range(0, movement_amount):
        x_coord += x_change
        y_coord += y_change
        wire.append((x_coord, y_coord))

    return process(wire, remaining_direction_changes, x_coord, y_coord)


def parse_wire(data: str) -> Wire:
    direction_changes: List[str] = data.split(',')

    x_coord = 0
    y_coord = 0

    wire: Wire = [(x_coord, y_coord)]

    return process(wire, direction_changes, x_coord, y_coord)


def parse(data: str) -> List[Wire]:
    return [parse_wire(x) for x in data.split('\n')]


if __name__ == "__main__":
    SOLVE(part_a, parse, True, [('R8,U5,L5,D3\nU7,R6,D4,L4', 6)])

    SOLVE(part_b, parse, True, [('R8,U5,L5,D3\nU7,R6,D4,L4', 30)])
