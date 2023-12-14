from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import as_complex_matrix_dict, to_2d_matrix, print_matrix_dict

input_data = get_puzzle_input()


def load_input(data):
    matrix = as_complex_matrix_dict(to_2d_matrix(data))
    # Throw away "."
    return {k: v for k, v in matrix.items() if v != "."}


def move_grid_north(grid):
    new_grid = {}
    max_y = max([int(x.imag) for x in grid.keys()])
    max_x = max([int(x.real) for x in grid.keys()])
    absent = object()  # Sentinel for not in grid

    moved = False
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            point = complex(x, y)
            val = grid.get(point, absent)
            if val == absent:
                continue  # Skip this point

            if val == "#":
                new_grid[point] = val
                continue  # Fixed rocks don't move

            new_point = point - 1j
            if new_point.real < 0 or new_point.imag < 0:
                new_point = point  # Point is at the top

            if grid.get(new_point, absent) in ["#", "O"]:
                new_grid[point] = val  # Can't move
            else:
                new_grid[new_point] = val
                moved = True

    # print_matrix_dict(new_grid)
    return new_grid, moved


def shift(grid):
    grid, moved = move_grid_north(grid)
    while moved:
        grid, moved = move_grid_north(grid)
    return grid


def print_matrix_dict(
    matrix,
    min_x,
    max_x,
    min_y,
    max_y,
    print_func=sprint,
):
    for y in range(min_y, max_y + 1):
        row_str = ""
        for x in range(min_x, max_x + 1):
            row_str += matrix.get(complex(x, y), " ")
        row_str += f" {y}"
        print_func(row_str)


@print_timings
def part_1():
    grid = load_input(input_data)

    min_x, max_x = min([int(x.real) for x in grid.keys()]), max(
        [int(x.real) for x in grid.keys()]
    )
    min_y, max_y = min([int(x.imag) for x in grid.keys()]), max(
        [int(x.imag) for x in grid.keys()]
    )

    print_matrix_dict(grid, min_x, max_x, min_y, max_y)
    sprint("-----")
    # move_grid_north(grid)
    grid = shift(grid)
    print_matrix_dict(grid, min_x, max_x, min_y, max_y)

    load = 0

    for point, val in grid.items():
        if val == "O":
            load += max_y + 1 - point.imag
    return int(load)


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)
