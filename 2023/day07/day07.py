from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from collections import defaultdict
from enum import Enum
from functools import cmp_to_key

input_data = get_puzzle_input()

CARD_STRENGTH = "AKQJT98765432"


class HandType(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7


def read_input(input_data):
    hands = []
    for line in input_data:
        hand, bet = line.split()
        bet = int(bet)
        hands.append((hand, bet))
    return hands


def parse_hand(hand):
    card_counts = defaultdict(int)
    for char in hand:
        card_counts[char] += 1
    return dict(card_counts)


def determine_type(cards):
    if 5 in cards.values():
        return HandType.FIVE_OF_A_KIND
    elif 4 in cards.values():
        return HandType.FOUR_OF_A_KIND
    elif 3 in cards.values() and 2 in cards.values():
        return HandType.FULL_HOUSE
    elif 3 in cards.values():
        return HandType.THREE_OF_A_KIND
    elif list(cards.values()).count(2) == 2:
        return HandType.TWO_PAIR
    elif 2 in cards.values():
        return HandType.ONE_PAIR
    else:
        return HandType.HIGH_CARD


def compare_hands(hand1_orig, hand2_orig):
    hand1_orig = hand1_orig[0]
    hand2_orig = hand2_orig[0]
    hand1 = parse_hand(hand1_orig)
    hand2 = parse_hand(hand2_orig)

    hand1_type = determine_type(hand1)
    hand2_type = determine_type(hand2)

    sprint("Hand 1:", hand1_orig, hand1_type, hand1_type.value)
    sprint("Hand 2:", hand2_orig, hand2_type, hand2_type.value)

    if hand1_type != hand2_type:
        return hand1_type.value - hand2_type.value

    # Tiebreak
    i = 0
    while hand1_orig[i] == hand2_orig[i]:
        i += 1

    return CARD_STRENGTH.index(hand1_orig[i]) - CARD_STRENGTH.index(hand2_orig[i])


@print_timings
def part_1():
    hands = read_input(input_data)
    sprint(hands)
    hands.sort(key=cmp_to_key(compare_hands))
    sprint(hands)

    total = 0
    for i, (hand, bet) in enumerate(reversed(hands)):
        rank = i + 1
        sprint("Hand:", hand, "Bet:", bet, "Rank:", rank)
        total += bet * rank
    return total


@print_timings
def part_2():
    pass


run(part_1, part_2)
