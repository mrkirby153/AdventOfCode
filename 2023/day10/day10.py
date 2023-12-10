from aoc_common import get_puzzle_input, run, sprint, parsed_args
from aoc_common.benchmark import print_timings
from aoc_common.io import to_2d_matrix, as_complex_matrix_dict, print_2d_matrix, numbers
from aoc_common.plane import neighbors
from aoc_common.ansi import colorize, RED, GREEN
from collections import defaultdict

input_data = get_puzzle_input()


DIRECTION_MAP = {1 + 0j: "W", -1 + 0j: "E", 1j: "N", -1j: "S"}

# A map of valid directions to enter a pipe
VALID_DIRECTIONS = {
    "|": "NS",
    "-": "EW",
    "L": "NE",
    "J": "NW",
    "7": "WS",
    "F": "SE",
    ".": "",
    "S": "NSEW",
}

# A map of valid directions to exit a pipe
VALID_EXIT_DIRECTIONS = {
    "|": "NS",
    "-": "EW",
    "L": "SW",
    "J": "SE",
    "7": "EN",
    "F": "NW",
    ".": "",
    "S": "NSEW",
}

BOXDRAW_CHARACTERS = {
    "|": "│",
    "-": "─",
    "L": "└",
    "J": "┘",
    "7": "┐",
    "F": "┌",
    ".": ".",
    "S": "S",
}


def load_data(input_data):
    return as_complex_matrix_dict(to_2d_matrix(input_data))


def find_starting_point(data):
    for point, value in data.items():
        if value == "S":
            return point


def get_next_pipes(data, point):
    sprint("At", point, data[point])
    neighboring_pipes = neighbors(point)

    valid_pipes = []
    for p in neighboring_pipes:
        if p not in data:
            continue
        delta = p - point
        direction = DIRECTION_MAP.get(delta, "")
        # sprint(f"Pipe", data[p], "is", direction)
        if direction in VALID_DIRECTIONS.get(
            data[p], ""
        ) and direction in VALID_EXIT_DIRECTIONS.get(data[point], ""):
            valid_pipes.append(p)
    return valid_pipes


def map_loop(data, start):
    loop_points = [start]
    next_pipe = get_next_pipes(data, start)[0]

    while next_pipe != start:
        loop_points.append(next_pipe)
        next = list(
            filter(lambda x: x not in loop_points, get_next_pipes(data, next_pipe))
        )
        if len(next) == 0:
            break
        assert len(next) == 1, f"Multiple next pipes found for {next_pipe}: {next}"
        next_pipe = next[0]
    return loop_points


def determine_furthest_point(loop_points):
    start = loop_points[0]

    loop_one = loop_points
    loop_two = list(reversed(loop_points[1:]))
    loop_two.insert(0, start)
    for i in range(len(loop_one)):
        if loop_one[i] == loop_two[i] and loop_one[i] != start:
            return i


def part_1_():
    debug_str = """At (25+42j) S
At (24+42j) L
At (24+41j) |
At (24+40j) F
At (25+40j) -
At (26+40j) J
At (26+39j) |
At (26+38j) 7
At (25+38j) F
At (25+39j) J
At (24+39j) L
At (24+38j) 7
At (23+38j) F
At (23+39j) |
At (23+40j) J
At (22+40j) L
At (22+39j) 7"""

    points = []
    for line in debug_str.split("\n"):
        point = numbers(line)
        print("line", point)
        points.append(complex(point[0], point[1]))
    print(points)

    graph = to_2d_matrix(input_data)
    data = load_data(input_data)

    def mapper(point, val):
        color = ""
        if point in points:
            color = RED
        return colorize(val, color)

    print_2d_matrix(
        graph,
        mapper=mapper,
    )


@print_timings
def part_1():
    graph = to_2d_matrix(input_data)
    data = load_data(input_data)
    start = find_starting_point(data)

    loop_points = map_loop(data, start)

    def mapper(point, val):
        color = ""
        if point in loop_points:
            color = RED
        if point == start:
            color = GREEN
        return colorize(val, color)

    print_2d_matrix(
        graph,
        print_func=sprint,
        mapper=mapper,
    )

    return determine_furthest_point(loop_points)


def get_shape_of_start(data, start):
    # |
    if (
        start + 1j in data
        and data[start + 1j] in "|LJ"
        and start - 1j in data
        and data[start - 1j] in "|7F"
    ):
        return "|"

    # -
    if (
        start - 1 in data
        and data[start - 1] in "-FL"
        and start + 1 in data
        and data[start + 1] in "-J7"
    ):
        return "-"

    # L
    if (
        start - 1j in data
        and data[start - 1j] in "|F7"
        and start + 1 in data
        and data[start + 1] in "-7J"
    ):
        return "L"
    # J
    if (
        start - 1j in data
        and data[start - 1j] in "|F7"
        and start - 1 in data
        and data[start - 1] in "-LF"
    ):
        return "J"
    # 7
    if (
        start + 1j in data
        and data[start + 1j] in "|LJ"
        and start - 1 in data
        and data[start - 1] in "-FL"
    ):
        return "7"
    # F
    if (
        start + 1j in data
        and data[start + 1j] in "|LJ"
        and start + 1 in data
        and data[start + 1] in "-J7"
    ):
        return "F"

    assert False, f"Could not determine shape of start {start}"


def count_inside_on_expanded(data):
    # Fill missing points with "."
    min_x, min_y = (
        int(min(data, key=lambda x: x.real).real),
        int(min(data, key=lambda x: x.imag).imag),
    )
    max_x, max_y = (
        int(max(data, key=lambda x: x.real).real),
        int(max(data, key=lambda x: x.imag).imag),
    )
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            point = complex(x, y)
            if point not in data:
                data[point] = "."

    count = 0
    for point, value in data.items():
        if point.real % 2 == 0 and point.imag % 2 == 0:
            sprint("Value", value)
            if value == ".":
                count += 1
    return count


def double_resolution(data):
    new_data = {}
    for k, v in data.items():
        new_data[k * 2 + 2j] = v

    max_x, max_y = (
        int(max(new_data, key=lambda x: x.real).real),
        int(max(new_data, key=lambda x: x.imag).imag),
    )

    # Go horizontal and connect all corners together
    new_horizontal_points = []
    for y in range(max_y + 1):
        start = None
        for x in range(max_x + 1):
            point = complex(x, y)
            curr = new_data.get(point, ".")
            if curr in ["F", "7", "L", "J"]:
                if start is None:
                    start = point
                else:
                    start = None
            else:
                if start is not None:
                    new_horizontal_points.append(complex(x, y))
    for point in new_horizontal_points:
        new_data[point] = "-"

    # Then go vertical and connect all corners together
    new_vertical_points = []
    for x in range(max_x + 1):
        start = None
        for y in range(max_y + 1):
            point = complex(x, y)
            curr = new_data.get(point, ".")
            if curr in ["F", "7", "L", "J"]:
                if start is None:
                    start = point
                else:
                    start = None
            else:
                if start is not None:
                    new_vertical_points.append(complex(x, y))
    for point in new_vertical_points:
        new_data[point] = "|"
    return new_data


def get_inside_count(data, points):
    # Discard all points outside the loop
    new_data = {}
    for point, value in data.items():
        if point in points:
            new_data[point] = value
    doubled = double_resolution(new_data)
    max_x, max_y = (
        int(max(doubled, key=lambda x: x.real).real),
        int(max(doubled, key=lambda x: x.imag).imag),
    )

    # Flood fill from the outside corners
    start_points = [
        complex(-1, -1),
        complex(-1, max_y + 1),
        complex(max_x + 1, -1),
        complex(max_x + 1, max_y + 1),
    ]

    outside_points = []

    queue = start_points.copy()
    while queue:
        print("Queue Length:", len(queue), end="\r")
        point = queue.pop(0)
        if point in outside_points:
            continue
        outside_points.append(point)
        next = neighbors(point)
        for p in next:
            if (
                p.real < 0 - 1
                or p.real > max_x + 2
                or p.imag < 0 - 1
                or p.imag > max_y + 2
            ):
                continue
            if doubled.get(p, ".") == ".":
                queue.append(p)
    print()
    orig_min_x, orig_min_y = (
        int(min(data, key=lambda x: x.real).real),
        int(min(data, key=lambda x: x.imag).imag),
    )
    orig_max_x, orig_max_y = (
        int(max(data, key=lambda x: x.real).real),
        int(max(data, key=lambda x: x.imag).imag),
    )

    # Figure out how many original points are not reachable from the outside

    # Translate from the original resolution to the doubled resolution
    original_points = []
    for y in range(orig_min_y, orig_max_y + 1):
        for x in range(orig_min_x, orig_max_x + 1):
            point = complex(x * 2, y * 2)
            original_points.append(point)

    # Get the values at the original points that are not marked as outside and count how many are "." (not a pipe)
    i = [doubled.get(p, ".") for p in original_points if p not in outside_points].count(
        "."
    )

    return i


@print_timings
def part_2():
    graph = to_2d_matrix(input_data)
    data = load_data(input_data)
    start = find_starting_point(data)

    loop_points = map_loop(data, start)

    data[start] = get_shape_of_start(data, start)

    def mapper(point, val):
        symbol = val
        if point not in loop_points:
            symbol = "."
        return BOXDRAW_CHARACTERS[val] if point in loop_points else symbol

    return get_inside_count(data, loop_points)


run(part_1, part_2)
