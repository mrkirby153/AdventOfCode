from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from collections import namedtuple
from aoc_common.io import print_matrix_dict, get_grid_dimensions
from tqdm import tqdm
from aoc_common.plane import neighbors

input_data = get_puzzle_input()


Instruction = namedtuple("Instruction", ["direction", "distance", "color"])


DIRECTIONS = {
    "U": -1j,
    "D": +1j,
    "L": -1,
    "R": +1,
}


def load_input(data):
    instructions = []
    for line in data:
        direction, distance, color = line.split()
        color = color[1:-2]
        instructions.append(Instruction(direction, int(distance), color))
    return instructions


def plot(instructions):
    current = complex(0, 0)
    grid = {}
    vertexes = set()
    for instruction in tqdm(instructions):
        sprint(f"Instruction: {instruction}")
        vertexes.add(current)
        for _ in range(instruction.distance):
            current += DIRECTIONS[instruction.direction]
            grid[current] = instruction.color
    return grid, vertexes


def find_first_inside_point(grid):
    (min_x, max_x), (min_y, max_y) = get_grid_dimensions(grid)
    for y in range(max_y + 1):
        walls = 0
        for x in range(max_x + 1):
            if grid.get(complex(x, y)) is not None:
                walls += 1
            else:
                print(f"Checking {x}, {y}", walls)
                if walls % 2 == 1:
                    return complex(x, y)
    return None


def flood_fill(grid, start):
    visited = set()

    queue = [start]
    while queue:
        point = queue.pop(0)
        if point in visited:
            continue
        visited.add(point)

        for p in neighbors(point):
            if grid.get(p) is None:
                queue.append(p)
    return visited


@print_timings
def part_1():
    instructions = load_input(input_data)
    plotted, vertexes = plot(instructions)

    inside = find_first_inside_point(plotted)
    sprint(f"Inside: {inside}")

    inside = flood_fill(plotted, inside)

    def _mapper(pos, val):
        if pos in vertexes:
            return "#"
        if pos in inside:
            return "#"
        return "#" if pos in plotted else "."

    print_matrix_dict(
        plotted,
        sprint,
        mapper=_mapper,
    )

    return len(inside) + len(plotted)


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)
