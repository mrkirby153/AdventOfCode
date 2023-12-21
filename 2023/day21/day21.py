from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import as_complex_matrix_dict, to_2d_matrix, print_matrix_dict
from aoc_common.plane import neighbors

input_data = get_puzzle_input()


def load_input(input_data):
    return as_complex_matrix_dict(to_2d_matrix(input_data))


def take_step(garden_map, points):
    reachable_points = set()

    for point in points:
        for neighbor in neighbors(point):
            if garden_map.get(neighbor) in ".S":
                reachable_points.add(neighbor)
    return reachable_points


def find_start(garden_map):
    for point, value in garden_map.items():
        if value == "S":
            return point


@print_timings
def part_1():
    garden_map = load_input(input_data)

    print_matrix_dict(garden_map, sprint)

    start = find_start(garden_map)
    assert start is not None, "No start found"

    points = {start}

    for _ in range(64):
        points = take_step(garden_map, points)

    def mapper(point, val):
        if point in points:
            return "O"
        return val

    print_matrix_dict(
        garden_map,
        sprint,
        mapper=mapper,
    )

    return len(points)


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)
