from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from collections import defaultdict
from enum import Enum
from functools import cmp_to_key, partial
from itertools import combinations_with_replacement

input_data = get_puzzle_input()

CARD_STRENGTH = "AKQJT98765432"
CARD_STRENGTH_JOKERS = "AKQT98765432J"


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


def find_most_common(hand):
    sprint("Finding most common in", hand)
    most_common = 0, None
    for card, count in hand.items():
        if card == "J":
            continue  # Don't include jokers
        if count > most_common[0]:
            most_common = count, card
    sprint("Most common:", most_common)
    return most_common


def count_jokers(hand):
    return hand.get("J", 0)


def is_full_house(hand):
    return 3 in hand.values() and 2 in hand.values()


def make_full_house(hand):
    sprint("Making full house from", hand)
    indicies = [i for i, card in enumerate(hand) if card == "J"]

    for combo in combinations_with_replacement("AKQT98765432", len(indicies)):
        full_house_hand = list(hand)
        for joker_index, replacement_card in zip(indicies, combo):
            sprint("Replacing", full_house_hand[joker_index], "with", replacement_card)
            full_house_hand[joker_index] = replacement_card
        if is_full_house(parse_hand(full_house_hand)):
            return full_house_hand
    return None


def optimize_hand(original_hand):
    hand = parse_hand(original_hand)
    sprint("Optimizing hand:", hand)
    if "J" not in hand:
        sprint("no jokers.")
        return hand
    # Should always take the card with the higest value
    # Try to make five of a kind
    count, most_common = find_most_common(hand)

    if count + count_jokers(hand) == 5:
        sprint("Otpimized to five of a kind")
        return {most_common: 5}

    if count + count_jokers(hand) == 4:
        sprint("Optimized to four of a kind")
        hand[most_common] = 4
        del hand["J"]
        return hand

    # Optimize to a full house
    full_house = make_full_house(original_hand)
    if full_house:
        sprint("Optimized to full house")
        return parse_hand(full_house)

    if count + count_jokers(hand) == 3:
        sprint("Optimized to three of a kind")
        hand[most_common] = 3
        del hand["J"]
        return hand

    # Optimize to two pair
    if count_jokers(hand) == 1:
        sprint("Optimized to two pair/one pair")
        del hand["J"]
        hand[most_common] = 2
        return hand

    return hand


def compare_hands(hand1_orig, hand2_orig, with_jokers=False):
    sprint("With jokers:", with_jokers)
    hand1_orig = hand1_orig[0]
    hand2_orig = hand2_orig[0]

    if with_jokers:
        hand1 = optimize_hand(hand1_orig)
        hand2 = optimize_hand(hand2_orig)
    else:
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

    strength = CARD_STRENGTH_JOKERS if with_jokers else CARD_STRENGTH

    return strength.index(hand1_orig[i]) - strength.index(hand2_orig[i])


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
    hands = read_input(input_data)
    sprint(hands)

    comp = partial(compare_hands, with_jokers=True)

    hands.sort(key=cmp_to_key(comp))
    sprint(hands)

    total = 0
    for i, (hand, bet) in enumerate(reversed(hands)):
        rank = i + 1
        sprint("Hand:", hand, "Bet:", bet, "Rank:", rank)
        total += bet * rank
    return total


run(part_1, part_2)
