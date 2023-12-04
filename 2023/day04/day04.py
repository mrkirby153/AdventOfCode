from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import numbers

input_data = get_puzzle_input()


def parse_card(card):
    winning_numbers, current_numbers = card.split("|")
    winning_numbers = numbers(winning_numbers)
    current_numbers = numbers(current_numbers)
    sprint("Winning Numbers:", winning_numbers, ", Current Numbers:", current_numbers)
    return winning_numbers, current_numbers


def get_winning_numbers(current_numbers, winning_numbers):
    return set(current_numbers).intersection(set(winning_numbers))


@print_timings
def part_1():
    total_score = 0
    for line in input_data:
        name, card = line.split(":")
        sprint("Processing", name)
        winning_numbers, current_numbers = parse_card(card)

        winning_numbers = get_winning_numbers(current_numbers, winning_numbers)
        sprint("Winning Numbers:", winning_numbers)

        score = 0
        if len(winning_numbers) > 0:
            score = 1
            for _ in range(len(winning_numbers) - 1):
                score *= 2
        sprint("Score:", score)
        total_score += score
    return total_score


@print_timings
def part_2():
    pass


run(part_1, part_2)
