from functools import partial
from os.path import basename, splitext
from typing import List, Tuple, Dict, Set

import networkx as nx  # type: ignore

from lib import solve

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)


def part_a(graph: nx.Graph) -> int:
    return sum(nx.shortest_path_length(graph, x, "COM") for x in graph.nodes)


def part_b(graph: nx.Graph) -> int:
    return nx.shortest_path_length(graph, "YOU", "SAN") - 2


def parse(data: str) -> nx.Graph:
    return nx.Graph([x.split(')') for x in data.split('\n')])


def get_indirect_orbits(direct_orbits, planet):
    if planet == 'COM':
        return []
    orbiting_around = direct_orbits[planet]
    return [orbiting_around] + get_indirect_orbits(direct_orbits, orbiting_around)


def part_a_no_nx(data: List[Tuple[str, str]]) -> int:
    planets: Set[str] = set([x for x, _ in data] + [y for _, y in data])

    direct_orbits: Dict[str, str] = {orbit_to: orbit_from for orbit_from, orbit_to in data}

    indirect_orbits: Dict[str, List[str]] = {
        planet: get_indirect_orbits(direct_orbits, planet) for planet in planets
    }

    indirect_orbits_count: int = sum([len(v) for v in indirect_orbits.values()])

    return indirect_orbits_count


def path_to_com(direct_orbits, origin):
    if origin == 'COM':
        return ['COM']
    return [origin] + path_to_com(direct_orbits, direct_orbits[origin])


def part_b_no_nx(data: List[Tuple[str, str]]) -> int:
    direct_orbits: Dict[str, str] = {orbit_to: orbit_from for orbit_from, orbit_to in data}

    you_path: List[str] = path_to_com(direct_orbits, 'YOU')
    santa_path = path_to_com(direct_orbits, 'SAN')

    intersection = set(you_path) & set(santa_path)

    first_intersection = [x for x in you_path if x in intersection][0]

    you_path_to_intersection = you_path[0:you_path.index(first_intersection)]
    santa_path_to_intersection = santa_path[0:santa_path.index(first_intersection)]

    path_to_santa = you_path_to_intersection + [first_intersection] + santa_path_to_intersection

    # 'YOU' and 'SANTA'
    path_to_santa.remove('YOU')
    path_to_santa.remove('SAN')

    # we count the transfers, so skip the last element
    return len(path_to_santa[0:-1])


def parse_no_nx(data: str) -> List[Tuple[str, str]]:
    return [(x.split(')')[0], x.split(')')[1]) for x in data.split('\n')]


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

    SOLVE(part_a_no_nx, parse_no_nx, False, [
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

    SOLVE(part_b_no_nx, parse_no_nx, False, [
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
