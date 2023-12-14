from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import as_complex_matrix_dict, to_2d_matrix
from tqdm import tqdm

input_data = get_puzzle_input()


def load_input(data):
    matrix = as_complex_matrix_dict(to_2d_matrix(data))
    # Throw away "."
    return {k: v for k, v in matrix.items() if v != "."}


def move_grid_north(grid, max_x, max_y):
    new_grid = {}
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


def move_grid_south(grid, max_x, max_y):
    new_grid = {}
    absent = object()  # Sentinel for not in grid

    moved = False
    for y in range(max_y, -1, -1):
        for x in range(0, max_x + 1):
            point = complex(x, y)
            val = grid.get(point, absent)
            if val == absent:
                continue  # Skip this point

            if val == "#":
                new_grid[point] = val
                continue  # Fixed rocks don't move

            new_point = point + 1j
            if new_point.imag > max_y:
                new_point = point  # Point is at the bottom

            if grid.get(new_point, absent) in ["#", "O"]:
                new_grid[point] = val  # Can't move
            else:
                new_grid[new_point] = val
                moved = True

    # print_matrix_dict(new_grid)
    return new_grid, moved


def move_grid_east(grid, max_x, max_y):
    new_grid = {}
    absent = object()  # Sentinel for not in grid

    moved = False
    for x in range(0, max_x + 1):
        for y in range(0, max_y + 1):
            point = complex(x, y)
            val = grid.get(point, absent)
            if val == absent:
                continue
            if val == "#":
                new_grid[point] = val
                continue

            new_point = point + complex(1, 0)
            if new_point.real > max_x:
                new_point = point

            if grid.get(new_point, absent) in ["#", "O"]:
                new_grid[point] = val
            else:
                new_grid[new_point] = val
                moved = True
    return new_grid, moved


def move_grid_west(grid, max_x, max_y):
    new_grid = {}
    absent = object()  # Sentinel for not in grid

    moved = False
    for x in range(max_x, -1, -1):
        for y in range(0, max_y + 1):
            point = complex(x, y)
            val = grid.get(point, absent)
            if val == absent:
                continue
            if val == "#":
                new_grid[point] = val
                continue

            new_point = point - complex(1, 0)
            if new_point.real < 0:
                new_point = point

            if grid.get(new_point, absent) in ["#", "O"]:
                new_grid[point] = val
            else:
                new_grid[new_point] = val
                moved = True
    return new_grid, moved


def perform_spin(grid, max_x, max_y):
    for func in [move_grid_north, move_grid_west, move_grid_south, move_grid_east]:
        grid = shift(grid, func, max_x, max_y)
    return grid


def hash_grid(grid):
    return frozenset((k.real, k.imag) for k in grid.keys())


def run_part_2(grid, max_x, max_y, num_cycles):
    lookup_map = {}
    hash_to_grid = {}

    for i in tqdm(range(num_cycles)):
        i += 1
        sprint("Cycle", i)
        grid = perform_spin(grid, max_x, max_y)
        # print_matrix_dict(grid, 0, max_x, 0, max_y)
        h = hash_grid(grid)
        if h in lookup_map:
            start = lookup_map[h]
            print("Found cycle. Current cycle:", i, "Last cycle:", lookup_map[h])
            cycle_length = i - lookup_map[h]
            print("Cycle length:", cycle_length)
            target = start + (num_cycles - start) % cycle_length
            target_hash = [k for k, v in lookup_map.items() if v == target][0]
            return hash_to_grid[target_hash]
        else:
            lookup_map[h] = i
            hash_to_grid[h] = grid
    return grid


def shift(grid, direction, max_x, max_y):
    orig_grid = grid
    grid, moved = direction(grid, max_x, max_y)
    while moved:
        grid, moved = direction(grid, max_x, max_y)

    assert len(grid) == len(orig_grid), "lost something"
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
            row_str += matrix.get(complex(x, y), ".")
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
    grid = shift(grid, move_grid_north, max_x, max_y)
    print_matrix_dict(grid, min_x, max_x, min_y, max_y)

    load = 0

    for point, val in grid.items():
        if val == "O":
            load += max_y + 1 - point.imag
    return int(load)


@print_timings
def part_2():
    grid = load_input(input_data)

    min_x, max_x = 0, max([int(x.real) for x in grid.keys()])
    min_y, max_y = 0, max([int(x.imag) for x in grid.keys()])

    print_matrix_dict(grid, min_x, max_x, min_y, max_y)

    # for i in tqdm(range(1000000000)):
    #     # sprint("Cycle", i)
    #     for func in [move_grid_north, move_grid_west, move_grid_south, move_grid_east]:
    #         # sprint(func)
    #         grid = shift(grid, func, max_x, max_y)
    #         # print_matrix_dict(grid, min_x, max_x, min_y, max_y)

    grid = run_part_2(grid, max_x, max_y, 1000000000)

    print_matrix_dict(grid, min_x, max_x, min_y, max_y)

    load = 0

    for point, val in grid.items():
        if val == "O":
            load += max_y + 1 - point.imag
    return int(load)


run(part_1, part_2, __name__)
