from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import (
    as_complex_matrix_dict,
    to_2d_matrix,
    get_grid_dimensions,
    print_matrix_dict,
)
from aoc_common.plane import neighbors as plane_neighbors
from aoc_common.ansi import colorize, RED
from collections import deque

input_data = get_puzzle_input()

DOWNHILL_DIRECTIONS = {
    ">": 1,
    "<": -1,
    "V:": 1j,
}


def load_input(input_data):
    return as_complex_matrix_dict(to_2d_matrix(input_data))


def find_start(grid):
    (min_x, max_x), (min_y, max_y) = get_grid_dimensions(grid)
    for x in range(max_x + 1):
        if grid[complex(x, 0)] == ".":
            return complex(x, 0)


def find_end(grid):
    (min_x, max_x), (min_y, max_y) = get_grid_dimensions(grid)
    for x in range(max_x + 1):
        if grid[complex(x, max_y)] == ".":
            return complex(x, max_y)


# def find_longest_path(grid, current, end, path=None):
#     if path is None:
#         path = []

#     if current == end:
#         return path

#     if current not in grid:
#         return []

#     downhill_direction = DOWNHILL_DIRECTIONS.get(grid.get(current, None), None)
#     if downhill_direction is not None:
#         sprint("must go downhill")
#         next_pos = current + downhill_direction
#         next_steps = [next_pos] if next_pos not in path else []
#     else:
#         next_steps = [n for n in neighbors(current)]
#         for n in next_steps:
#             sprint("checking", n, grid.get(n, None), n in path)
#         next_steps = [
#             n for n in next_steps if n not in path and grid.get(n, None) != "#"
#         ]
#     sprint("at", current, "next steps", next_steps)

#     def _mapper(k, v):
#         if k == current:
#             return "O"
#         elif k in path:
#             return "X"
#         return v

#     print_matrix_dict(grid, sprint, _mapper)
#     if len(next_steps) == 0:
#         return []  # no path found
#     return max(
#         [find_longest_path(grid, n, end, path + [n]) for n in next_steps],
#         key=len,
#     )


def neighbors(grid, pos):
    if grid[pos] == "v":
        yield pos + 1j
        return
    elif grid[pos] == "^":
        yield pos - 1j
        return
    elif grid[pos] == ">":
        yield pos + 1
        return
    elif grid[pos] == "<":
        yield pos - 1
        return

    for n in plane_neighbors(pos):
        if n in grid and grid[n] != "#":
            yield n


def find_longest_path(grid, start, end):
    queue = deque([(start, set())])
    costs = dict()
    costs[start] = 0
    while queue:
        print("queue", len(queue), end="\r")
        pos, path = queue.pop()
        if pos == end:
            continue
        for n in neighbors(grid, pos):
            new_cost = costs[pos] + 1
            if n in path:
                continue  # already visited
            if n not in costs or new_cost > costs[n]:
                costs[n] = new_cost
                new_path = path.copy()
                new_path.add(n)
                queue.appendleft((n, new_path))
    return costs[end]


@print_timings
def part_1():
    grid = load_input(input_data)
    start = find_start(grid)
    end = find_end(grid)
    return find_longest_path(grid, start, end)


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)
