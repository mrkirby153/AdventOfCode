from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import to_2d_matrix, as_complex_matrix_dict, print_2d_matrix, numbers
from aoc_common.plane import neighbors
from aoc_common.ansi import colorize, RED, GREEN

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


@print_timings
def part_2():
    pass


run(part_1, part_2)
