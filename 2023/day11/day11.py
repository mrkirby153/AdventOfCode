from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import as_complex_matrix_dict, to_2d_matrix
from itertools import combinations

input_data = get_puzzle_input()


def load_data(input_data):
    return as_complex_matrix_dict(to_2d_matrix(input_data))


def expand_universe(data, times=1):
    data2 = {}
    for k, v in data.items():
        if v != ".":
            data2[k] = v
    total_points = len(data2.keys())  # Keep track so we don't lose any
    data = data2
    min_x, max_x = int(min(p.real for p in data)), int(max(p.real for p in data))
    min_y, max_y = int(min(p.imag for p in data)), int(max(p.imag for p in data))

    # Identify all horizontal rows
    horizontal_empty_rows = []
    for y in range(min_y, max_y + 1):
        valid = True
        for x in range(min_x, max_x + 1):
            point = complex(x, y)
            if point not in data:
                continue
            if data[point] != ".":
                valid = False
        if valid:
            horizontal_empty_rows.append(y)
    vertical_empty_rows = []
    for x in range(min_x, max_x + 1):
        valid = True
        for y in range(min_y, max_y + 1):
            point = complex(x, y)
            if point not in data:
                continue
            sprint(point, data[point])
            if data[point] != ".":
                valid = False
        if valid:
            vertical_empty_rows.append(x)

    sprint("Horizontal empty rows", horizontal_empty_rows)
    sprint("Vertical empty rows", vertical_empty_rows)

    # Expand all horizontal rows

    horiz_map = {x: x for x in horizontal_empty_rows}

    for horiz in horizontal_empty_rows:
        print("Expanding row", horiz, horiz_map[horiz])
        horiz = horiz_map[horiz]  # Account for the fact that we're adding rows
        new_data = {}
        # Move all points below this row down n times
        for point, value in data.items():
            x, y = int(point.real), int(point.imag)
            if y < horiz:
                new_data[point] = value  # Does not change
            else:
                new_data[point + complex(0, times)] = value
        # Increase max_y
        max_y += times
        assert (
            len(new_data.keys()) == total_points
        ), f"Lost points: Expected {total_points}, got {len(new_data.keys())}"
        # Update data
        data = new_data

        # Adjust horiz_map and increase all values above this row by one
        for row in horiz_map:
            if horiz_map[row] > horiz:
                horiz_map[row] += times

    # Expand all vertical rows
    vert_map = {x: x for x in vertical_empty_rows}
    for vert in vertical_empty_rows:
        print("Expanding column", vert, vert_map[vert])
        original_vert = vert
        vert = vert_map[vert]
        new_data = {}
        for point, value in data.items():
            x, y = int(point.real), int(point.imag)
            if x < vert:
                new_data[point] = value
            else:
                new_data[point + complex(times, 0)] = value
        max_x += times
        data = new_data

        for col in vert_map:
            if vert_map[col] > vert:
                vert_map[col] += times
        # print("vert", vert_map)

    # for y in range(min_y, max_y + 1):
    #     for x in range(min_x, max_x + 1):
    #         point = complex(x, y)
    #         sprint(data.get(point, "."), end="")
    #     sprint()
    return data


def map_pairs(data):
    numbered_points = {}
    num = 1
    for point, value in data.items():
        if value != ".":
            numbered_points[num] = point
            num += 1
    return numbered_points, list(combinations(numbered_points.keys(), 2))


def get_distance_between_points(point1, point2):
    return int(abs(point1.real - point2.real) + abs(point1.imag - point2.imag))


@print_timings
def part_1():
    data = load_data(input_data)

    data = expand_universe(data)
    points, combinations = map_pairs(data)

    distance = 0
    for p1, p2 in combinations:
        distance += get_distance_between_points(points[p1], points[p2])
    return distance


@print_timings
def part_2():
    data = load_data(input_data)

    actual = 1_000_000 - 1
    data = expand_universe(data, actual)
    points, combinations = map_pairs(data)

    distance = 0
    for p1, p2 in combinations:
        distance += get_distance_between_points(points[p1], points[p2])
    return distance


run(part_1, part_2)
