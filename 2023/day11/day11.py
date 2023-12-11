from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import as_complex_matrix_dict, to_2d_matrix
from itertools import combinations

input_data = get_puzzle_input()


def load_data(input_data):
    return as_complex_matrix_dict(to_2d_matrix(input_data))


def expand_universe(data):
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
            print(point, data[point])
            if data[point] != ".":
                valid = False
        if valid:
            vertical_empty_rows.append(x)

    sprint("Horizontal empty rows", horizontal_empty_rows)
    sprint("Vertical empty rows", vertical_empty_rows)

    # Expand all horizontal rows

    horiz_map = {x: x for x in horizontal_empty_rows}

    for horiz in horizontal_empty_rows:
        sprint("Expanding row", horiz)
        horiz = horiz_map[horiz]  # Account for the fact that we're adding rows
        new_data = dict(data)
        # Move all points below this row down by one
        for y in range(horiz, max_y + 1):
            for x in range(min_x, max_x + 1):
                point = complex(x, y)
                if point not in data:
                    continue
                new_data[point + 1j] = data[point]
        # Increase max_y
        max_y += 1
        # Update data
        data = new_data

        # Adjust horiz_map and increase all values above this row by one
        for row in horiz_map:
            if row > horiz:
                horiz_map[row] += 1

    # Expand all vertical rows
    vert_map = {x: x for x in vertical_empty_rows}
    for vert in vertical_empty_rows:
        sprint("Expanding column", vert)
        vert = vert_map[vert]
        new_data = dict(data)
        for x in range(vert, max_x + 1):
            for y in range(min_y, max_y + 1):
                point = complex(x, y)
                if point not in data:
                    continue
                new_data[point + 1] = data[point]
        max_x += 1
        data = new_data

        for col in vert_map:
            if col > vert:
                vert_map[col] += 1

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            point = complex(x, y)
            assert point in data, f"Point {point} not in data"
            sprint(data[point], end="")
        sprint()
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

    # shortest = {}
    # for p1, p2 in combinations:
    #     distance = get_distance_between_points(points[p1], points[p2])
    #     shortest[p1] = min(shortest.get(p1, 99999999), distance)
    #     shortest[p2] = min(shortest.get(p2, 99999999), distance)
    # print(shortest)
    # return sum(shortest.values())
    distance = 0
    for p1, p2 in combinations:
        distance += get_distance_between_points(points[p1], points[p2])
    return distance


@print_timings
def part_2():
    pass


run(part_1, part_2)
