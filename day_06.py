from functools import partial
from os.path import basename, splitext
from typing import List, Tuple, Dict, Set

import networkx as nx

from lib import solve

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)


def part_a(graph: nx.Graph) -> int:

    return sum(nx.shortest_path_length(graph, x, "COM") for x in graph.nodes)


def part_b(graph: nx.Graph) -> int:

    return nx.shortest_path_length(graph, "YOU", "SAN") - 2


def parse(data: str) -> nx.Graph:
    return nx.Graph([x.split(')') for x in data.split('\n')])


if __name__ == "__main__":
    SOLVE(part_a, parse, False, [
        ('''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L''', 42),
        ('''COM)A
A)B''', 3)
    ])

    SOLVE(part_b, parse, False, [
        ('''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN''', 4)
    ])
