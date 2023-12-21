from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import (
    as_complex_matrix_dict,
    to_2d_matrix,
    print_matrix_dict,
    get_grid_dimensions,
)
from aoc_common.plane import neighbors
from tqdm import tqdm

input_data = get_puzzle_input()


def load_input(input_data):
    return as_complex_matrix_dict(to_2d_matrix(input_data))


def take_step(garden_map, points, x_dim, y_dim):
    reachable_points = set()

    for point in points:
        for neighbor in neighbors(point):
            if garden_map[map_points(neighbor, x_dim, y_dim)] in ".S":
                reachable_points.add(neighbor)
    return reachable_points


def find_start(garden_map):
    for point, value in garden_map.items():
        if value == "S":
            return point


def map_points(point, x_dim, y_dim):
    (min_x, max_x), (min_y, max_y) = x_dim, y_dim

    # The grid repeats indefinitely, so we need to map the point to the
    # smallest positive value
    x = point.real % (max_x - min_x + 1)
    y = point.imag % (max_y - min_y + 1)
    return complex(x, y)


@print_timings
def part_1():
    garden_map = load_input(input_data)

    print_matrix_dict(garden_map, sprint)

    start = find_start(garden_map)
    assert start is not None, "No start found"

    x_dim, y_dim = get_grid_dimensions(garden_map)

    points = {start}

    for _ in range(64):
        points = take_step(garden_map, points, x_dim, y_dim)

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


def interpolate(poly, n):
    b0 = poly[0]
    b1 = poly[1] - poly[0]
    b2 = poly[2] - poly[1]
    return b0 + b1 * n + (n * (n - 1) // 2) * (b2 - b1)


@print_timings
def part_2():
    garden_map = load_input(input_data)

    start = find_start(garden_map)
    assert start is not None, "No start found"

    x_dim, y_dim = get_grid_dimensions(garden_map)

    width = x_dim[1] - x_dim[0] + 1
    steps = 26501365
    accumulated = []

    for step in [65, 65 + 131, 65 + 131 * 2]:
        points = {start}
        for _ in tqdm(range(step)):
            points = take_step(garden_map, points, x_dim, y_dim)
        accumulated.append(len(points))
    return interpolate(accumulated, steps // width)


run(part_1, part_2, __name__)
