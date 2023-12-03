from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import to_2d_matrix
import re
import operator
from functools import reduce

input_data = get_puzzle_input()

input_data_matrix = to_2d_matrix(input_data)

sprint(input_data_matrix)

digit_re = re.compile(r"\d+")


def adjacent(num):
    for x in range(-1, 2):
        for y in range(-1, 2):
            yield complex(x, y) + num


def process_line(line_num, matrix):
    line = input_data[line_num]
    sprint(f"Processing line {line}")
    valid_part_numbers = []
    for match in digit_re.finditer(line):
        sprint(f"Processing match: {match}")
        start, end = match.span()
        to_check = list(map(lambda x: complex(x, line_num), range(start, end)))
        sprint(f"Checking {to_check}")

        for num in to_check:
            should_break = False
            for point in adjacent(num):
                if point == num:
                    continue  # skip self
                x, y = int(point.real), int(point.imag)
                if x < 0 or y < 0 or x >= len(matrix[0]) or y >= len(matrix):
                    sprint(f"{x}, {y} is out of bounds")
                    continue
                actual = matrix[y][x]
                sprint(f"{x}, {y} is {actual}")
                if not (actual >= "0" and actual <= "9") and actual != ".":
                    sprint(f"Valid! {match.group()}")
                    valid_part_numbers.append(int(match.group()))
                    should_break = True
                    break

            if should_break:  # break out of outer loop
                break
    return valid_part_numbers


@print_timings
def part_1():
    valid_numbers = []
    for i in range(len(input_data_matrix)):
        valid_numbers.extend(process_line(i, input_data_matrix))
    sprint(f"Valid Numbers: {valid_numbers}")
    return reduce(operator.add, valid_numbers)


@print_timings
def part_2():
    pass


run(part_1, part_2)
