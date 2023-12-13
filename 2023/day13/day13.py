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


def find_differences(pattern_1, pattern_2):
    assert len(pattern_1) == len(pattern_2)
    return sum([1 for x in range(len(pattern_1)) if pattern_1[x] != pattern_2[x]])


def print_pattern(pattern, print_func=sprint):
    max_x = max([int(x.real) for x in pattern.keys()]) + 1
    max_y = max([int(x.imag) for x in pattern.keys()]) + 1
    for y in range(0, max_y):
        print_func("".join([pattern[x + y * 1j] for x in range(0, max_x)]))


def find_h_reflection(pattern, max_differences=0):
    max_y = max([int(x.imag) for x in pattern.keys()])

    for y in range(0, max_y):
        top_trace, bottom_trace = y, y + 1
        differences = 0
        while top_trace >= 0 and bottom_trace <= max_y:
            r1 = get_row(pattern, top_trace)
            r2 = get_row(pattern, bottom_trace)
            d = find_differences(r1, r2)
            differences += d

            top_trace -= 1
            bottom_trace += 1
        if differences == max_differences:
            return y
    return None


def find_v_reflection(pattern, max_differences=0):
    max_x = max([int(x.real) for x in pattern.keys()])

    for x in range(0, max_x):
        left_trace, right_trace = x, x + 1
        differences = 0
        while left_trace >= 0 and right_trace <= max_x:
            c1 = get_column(pattern, left_trace)
            c2 = get_column(pattern, right_trace)
            d = find_differences(c1, c2)
            differences += d

            left_trace -= 1
            right_trace += 1
        if differences == max_differences:
            return x
    return None


@print_timings
def part_1():
    patterns = load_data(input_data)

    acc = 0
    for i, pattern in enumerate(patterns):
        vert = find_v_reflection(pattern)
        horz = find_h_reflection(pattern)
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
    patterns = load_data(input_data)

    pattern = patterns[0]
    print_pattern(pattern, print)

    acc = 0
    for i, pattern in enumerate(patterns):
        vert = find_v_reflection(pattern, 1)
        horz = find_h_reflection(pattern, 1)
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


run(part_1, part_2, __name__)
