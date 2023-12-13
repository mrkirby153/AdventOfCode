from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import to_2d_matrix, as_complex_matrix_dict

input_data = get_puzzle_input()


def load_data(input_data):
    patterns = []

    pattern_buffer = []
    for line in input_data:
        if line != "":
            pattern_buffer.append(line)
        else:
            patterns.append(pattern_buffer)
            pattern_buffer = []
    if len(pattern_buffer) > 0:
        patterns.append(pattern_buffer)

    return list(map(as_complex_matrix_dict, map(to_2d_matrix, patterns)))


def get_column(pattern, column):
    max_y = max([int(x.imag) for x in pattern.keys()]) + 1
    return [pattern[complex(column, y)] for y in range(0, max_y)]


def get_row(pattern, row):
    max_x = max([int(x.real) for x in pattern.keys()]) + 1
    return [pattern[complex(x, row)] for x in range(0, max_x)]


def find_vertical_reflection(pattern):
    # Go pairwise through the pattern and check for two rows that are the same
    max_x = max([int(x.real) for x in pattern.keys()])
    max_y = max([int(x.imag) for x in pattern.keys()])

    is_odd = (max_x + 1) % 2 == 1
    for x in range(0, max_x):
        sprint()
        # Get the two rows
        row_1 = get_column(pattern, x)
        row_2 = get_column(pattern, x + 1)
        sprint(x, row_1)
        sprint(x + 1, row_2)
        if row_1 == row_2:
            sprint("Found vertical reflection candidate at rows", x, x + 1)

            left_trace, right_trace = x, x + 1
            valid = True
            while valid:
                print("left", left_trace, "right", right_trace)
                print("max", max_x)
                if right_trace == max_x:
                    allowed_top = 1 if is_odd else 0
                    print("allowed top", allowed_top)
                    return x if left_trace == allowed_top else None
                if left_trace == 0:
                    valid = False
                    break

                if list(get_column(pattern, left_trace)) != list(
                    get_column(pattern, right_trace)
                ):
                    sprint("not valid")
                    valid = False
                    break
                left_trace -= 1
                right_trace += 1
    return None


def print_pattern(pattern, print_func=sprint):
    max_x = max([int(x.real) for x in pattern.keys()]) + 1
    max_y = max([int(x.imag) for x in pattern.keys()]) + 1
    for y in range(0, max_y):
        print_func("".join([pattern[x + y * 1j] for x in range(0, max_x)]))


def find_horizontal_reflection(pattern):
    max_x = max([int(x.real) for x in pattern.keys()])
    max_y = max([int(x.imag) for x in pattern.keys()])

    is_odd = (max_y + 1) % 2 == 1

    for y in range(0, max_y):
        sprint()
        row_1 = list(get_row(pattern, y))
        row_2 = list(get_row(pattern, y + 1))
        sprint(row_1)
        sprint(row_2)
        if row_1 == row_2:
            sprint("Found horizontal reflection candidate at rows", y, y + 1)

            top_trace, bottom_trace = y, y + 1
            valid = True

            while valid:
                print("top", top_trace, "bottom", bottom_trace)
                print("max", max_y)
                if bottom_trace == max_y:
                    # At the bottom of the pattern, if this pattern is odd, we can ignore the first row
                    allowed_top = 1 if is_odd else 0
                    print("allowed top", allowed_top)
                    return y if top_trace == allowed_top else None
                if top_trace == 0:
                    valid = False
                    break

                if list(get_row(pattern, top_trace)) != list(
                    get_row(pattern, bottom_trace)
                ):
                    sprint("not valid")
                    valid = False
                    break
                top_trace -= 1
                bottom_trace += 1
    return None


@print_timings
def part_1():
    patterns = load_data(input_data)
    # t = patterns[0]

    # print_pattern(t)
    # return find_vertical_reflection(t)
    # print_pattern(patterns[1])
    # # # !!! THESE REFLECTION ROWS ARE ZERO INDEXED !!!
    # return find_vertical_reflection(patterns[1])
    acc = 0
    for i, pattern in enumerate(patterns[1:]):
        vert = find_vertical_reflection(pattern)
        horz = find_horizontal_reflection(pattern)
        if vert is not None and horz is not None:
            print(f"PATTERN {i} HAS BOTH REFLECTIONS", vert, horz)
            print_pattern(pattern, print)
            return

        if vert is not None:
            acc += vert + 1
        elif horz is not None:
            acc += (horz + 1) * 100
        else:
            print(f"PATTERN {i} HAS NO REFLECTIONS")
            print_pattern(pattern, print)
            return
    return acc


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)
