from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import numbers

input_data = get_puzzle_input()


def load_input(input_data):
    return [numbers(x) for x in input_data]


def generate_next_sequence(numbers):
    sequence = []
    for i in range(1, len(numbers)):
        sequence.append(numbers[i] - numbers[i - 1])
    return sequence


def is_terminal(sequence):
    return all([x == 0 for x in sequence])


def expand_sequence(sequence):
    sprint("Expanding", sequence)
    full = [sequence]
    seq = sequence
    while not is_terminal(seq):
        seq = generate_next_sequence(seq)
        sprint("Next sequence", seq)
        full.append(seq)

    return full


def extrapolate_sequence(sequence):
    assert is_terminal(sequence[-1]), "Sequence must be terminal"

    sequence = sequence.copy()
    sequence[-1].append(0)

    for i in range(len(sequence) - 2, -1, -1):
        sprint("extrapolating row", sequence[i], "prev:", sequence[i + 1])
        next_seq = sequence[i][-1] + sequence[i + 1][-1]
        sequence[i].append(next_seq)
        sprint("extrapolated row", sequence[i])
    return sequence


def process_sequence(sequence):
    expanded = expand_sequence(sequence)
    extrapolated = extrapolate_sequence(expanded)
    return extrapolated


@print_timings
def part_1():
    total = 0
    sequences = load_input(input_data)
    for sequence in sequences:
        sprint("Processing sequence", sequence)
        expanded = expand_sequence(sequence)
        extrapolated = extrapolate_sequence(expanded)[0]
        assert len(expanded) == len(
            expand_sequence(extrapolated)
        ), f"Extrapolation failed for {sequence}"
        total += extrapolated[-1]
    return total


@print_timings
def part_2():
    pass


run(part_1, part_2)
