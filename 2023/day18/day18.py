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


def load_input_2(data):
    instructions = []
    for line in data:
        code = line.split()[-1][2:-1]
        sprint("Code", code)
        distance = int(code[:-1], 16)
        direction = code[-1]
        if direction == "0":
            direction = "R"
        elif direction == "1":
            direction = "D"
        elif direction == "2":
            direction = "L"
        elif direction == "3":
            direction = "U"
        else:
            assert False, f"Unknown direction {direction}"
        instructions.append(
            Instruction(direction, distance, "black")
        )  # We don't care about color, actually lol
    return instructions


def plot(instructions):
    current = complex(0, 0)
    vertexes = []
    line_length = 0
    for instruction in tqdm(instructions):
        sprint(f"Instruction: {instruction}")
        vertexes.append(current)
        current += DIRECTIONS[instruction.direction] * instruction.distance
        line_length += instruction.distance
    return vertexes, (line_length // 2 + 1)


# From https://stackoverflow.com/a/24468019
def poly_area(poly):
    area = 0.0
    for i in range(len(poly)):
        j = (i + 1) % len(poly)
        area += poly[i].real * poly[j].imag
        area -= poly[j].real * poly[i].imag
    area = abs(area) / 2.0
    return area


@print_timings
def part_1():
    instructions = load_input(input_data)
    plotted, border_length = plot(instructions)

    return poly_area(plotted) + border_length


@print_timings
def part_2():
    instructions = load_input_2(input_data)
    plotted, border_length = plot(instructions)

    return poly_area(plotted) + border_length


run(part_1, part_2, __name__)
