import re

def to_2d_matrix(raw_input, mapper=None):
    """
    Reads a raw input into a 2d matrix
    """
    return [[y if mapper is None else mapper(y) for y in x] for x in raw_input]

def print_2d_matrix(matrix, print_func=print, mapper=None, pad=False):
    """
    Prints out a 2d matrix
    """
    def _map(val):
        return val if mapper is None else mapper(val)
    max_width = 0
    if pad:
        raw = [_map(y) for x in matrix for y in x]
        max_width = max([len(x) for x in raw])
    for row in matrix:
        row_str = ""
        for col in row:
            value = str(_map(col))
            while pad and len(value) < max_width:
                value = f" {value}"
            row_str += value
            if pad:
                row_str += " "
        print_func(row_str)

_number_regex = re.compile(r"\d+(?:\.\d+)?")

def numbers(line):
    """
    Extracts all numbers from the given line of text
    """
    groups = _number_regex.findall(line)
    return [int(number) if '.' not in number else float(number) for number in groups]