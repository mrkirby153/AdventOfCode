from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import numbers
from functools import lru_cache

input_data = get_puzzle_input()


@lru_cache
def parse_card(card):
    winning_numbers, current_numbers = card.split("|")
    winning_numbers = numbers(winning_numbers)
    current_numbers = numbers(current_numbers)
    sprint("Winning Numbers:", winning_numbers, ", Current Numbers:", current_numbers)
    return frozenset(winning_numbers), frozenset(current_numbers)


@lru_cache
def get_winning_numbers(current_numbers, winning_numbers):
    return current_numbers.intersection(winning_numbers)


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
    num_cards = {}
    cards = {}
    for line in input_data:
        name, card = line.split(":")
        card_num = numbers(name)[0]
        winning_numbers, current_numbers = parse_card(card)

        winning_numbers = get_winning_numbers(current_numbers, winning_numbers)
        cards[card_num] = winning_numbers
        num_cards[card_num] = 1
    sprint("num_cards", num_cards)
    sprint("cards", cards)
    for card_num in range(1, max(num_cards.keys()) + 1):
        sprint("Processing card", card_num)
        num_cards_won = len(cards[card_num])
        card_numbers_won = range(card_num + 1, card_num + num_cards_won + 1)
        sprint(
            "It has ",
            num_cards_won,
            "winning numbers, so it wins cards ",
            list(card_numbers_won),
        )
        total_cards = num_cards[card_num]
        for c in card_numbers_won:
            num_cards[c] += total_cards
    return sum(num_cards.values())


run(part_1, part_2)
