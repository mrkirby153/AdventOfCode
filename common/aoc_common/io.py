import re


def to_2d_matrix(raw_input, mapper=None):
    """
    Reads a raw input into a 2d matrix
    """
    return [[y if mapper is None else mapper(y) for y in x] for x in raw_input]


def as_complex_matrix_dict(matrix):
    """
    Converts a matrix into a dict of complex numbers to values with 0, 0 being the top left
    """
    return {
        complex(x, y): matrix[y][x]
        for y in range(len(matrix))
        for x in range(len(matrix[y]))
    }


def print_2d_matrix(matrix, print_func=print, mapper=None, pad=False):
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


_number_regex = re.compile(r"\d+(?:\.\d+)?")
_negative_number_regex = re.compile(r"-?\d+(?:\.\d+)?")
_single_number_regex = re.compile(r"\d")
_negative_single_number_regex = re.compile(r"-?\d")


def numbers(line, single=False, with_negatives=True):
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
