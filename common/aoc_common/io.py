import re
from typing import Any, Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def to_2d_matrix(raw_input, mapper=None):
    """
    Reads a raw input into a 2d matrix
    """
    return [[y if mapper is None else mapper(y) for y in x] for x in raw_input]


def as_complex_matrix_dict(matrix: list[list[T]]):
    """
    Converts a matrix into a dict of complex numbers to values with 0, 0 being the top left
    """
    return {
        complex(x, y): matrix[y][x]
        for y in range(len(matrix))
        for x in range(len(matrix[y]))
    }


def print_2d_matrix(
    matrix: list[list[T]],
    print_func=print,
    mapper: Callable[[complex, T], U] = None,
    pad=False,
):
    """
    Prints out a 2d matrix
    """

    def _map(point, val):
        return val if mapper is None else mapper(point, val)

    max_width = 0
    if pad:
        raw = [_map(y) for x in matrix for y in x]
        max_width = max([len(x) for x in raw])
    for y, row in enumerate(matrix):
        row_str = ""
        for x, col in enumerate(row):
            value = str(_map(complex(x, y), col))
            while pad and len(value) < max_width:
                value = f" {value}"
            row_str += value
            if pad:
                row_str += " "
        print_func(row_str)


def print_matrix_dict(
    matrix: dict[complex, T],
    print_func=print,
    mapper: Callable[[complex, T], U] = None,
    pad=False,
    empty: T = ".",
):
    """
    Prints out a 2d matrix represented as a dict of complex numbers to values
    """

    def _map(point, val: T):
        return val if mapper is None else mapper(point, val)

    max_width = 0
    if pad:
        raw = [_map(p, v) for p, v in matrix.items()]
        max_width = max([len(str(x)) for x in raw])

    for y in range(max([int(p.imag) for p in matrix.keys()]) + 1):
        row_str = ""
        for x in range(max([int(p.real) for p in matrix.keys()]) + 1):
            value = str(_map(complex(x, y), matrix.get(complex(x, y), empty)))
            while pad and len(value) < max_width:
                value = f" {value}"
            row_str += value
            if pad:
                row_str += " "
        print_func(row_str)


def get_grid_dimensions(
    grid: dict[complex, Any]
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Gets the min and max x and y values from a grid
    """
    min_x, max_x = min([int(x.real) for x in grid.keys()]), max(
        [int(x.real) for x in grid.keys()]
    )
    min_y, max_y = min([int(x.imag) for x in grid.keys()]), max(
        [int(x.imag) for x in grid.keys()]
    )
    return (min_x, max_x), (min_y, max_y)


_number_regex = re.compile(r"\d+(?:\.\d+)?")
_negative_number_regex = re.compile(r"-?\d+(?:\.\d+)?")
_single_number_regex = re.compile(r"\d")
_negative_single_number_regex = re.compile(r"-?\d")


def numbers(line: str, single=False, with_negatives=True):
    """
    Extracts all numbers from the given line of text. Pass `single` to only extract single digit numbers.
    """
    single_re = (
        _negative_single_number_regex if with_negatives else _single_number_regex
    )
    number_re = _negative_number_regex if with_negatives else _number_regex

    regex = single_re if single else number_re
    groups = regex.findall(line)
    return [int(number) if "." not in number else float(number) for number in groups]


def collapse_range(r):
    """
    Collapses a list of numbers into ranges
    """
    ranges = []

    for n in sorted(r):
        if not ranges or n > ranges[-1][-1] + 1:
            ranges.append([])
        ranges[-1][1:] = (n,)
    if len(ranges) == 1:
        return ranges[0]
    return ranges
