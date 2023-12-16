from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import as_complex_matrix_dict, to_2d_matrix, print_matrix_dict
from collections import defaultdict
from aoc_common.ansi import colorize, RED

input_data = get_puzzle_input()

# Maps current direction to the next direction
MAP_DIRECTIONS = {
    "\\": {(1): [(0 + 1j)], (0 - 1j): [(-1)], (-1): [(0 - 1j)], (0 + 1j): [(1)]},
    "/": {(1): [(0 - 1j)], (-1): [(0 + 1j)], (0 + 1j): [(-1)], (0 - 1j): [(1)]},
    "|": {
        (1): [(0 + 1j), (0 - 1j)],
        (-1): [(0 + 1j), (0 - 1j)],
        # (0 + 1j): [0],
        # (0 - 1j): [0],
    },
    "-": {
        # (1): [0],
        # (-1): [0],
        (0 + 1j): [-1, 1],
        (0 - 1j): [-1, 1],
    },
}


def load_data(input_data):
    return as_complex_matrix_dict(to_2d_matrix(input_data))


def trace_laser(start, grid, direction=1):
    queue = [(start, direction)]
    visited = defaultdict(set)

    v2 = set()

    while queue:
        sprint("----")
        current, direction = queue.pop()
        sprint(f"Current: {current}, Direction: {direction}")

        beams_visited = visited[current]

        if (
            current not in grid or direction in beams_visited
        ):  # This beam has already visited this point going this direction
            continue

        beams_visited.add(direction)  # Mark this point as visited in this direction
        v2.add(current)

        curr = grid.get(current, ".")
        if curr == ".":
            # Continue our current direction
            queue.append((current + direction, direction))
        else:
            sprint("Updating direction", curr, direction)
            direction_map = MAP_DIRECTIONS[curr].get(direction, None)
            sprint("New directions", direction_map)
            if direction_map is not None:
                queue.extend([(current + d, d) for d in direction_map])
            else:
                # Continue our current direction
                queue.append((current + direction, direction))

    return v2


@print_timings
def part_1():
    grid = load_data(input_data)

    return len(trace_laser(0, grid))


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)
