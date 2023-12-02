from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import numbers
import re
from functools import reduce
import operator

input_data = get_puzzle_input()

round_re = re.compile(r"(\d+) (blue|red|green)")


def process_input(input_data):
    games = []  # (game_id, [rounds])
    for line in input_data:
        header, rounds = line.split(":")
        rounds = rounds.strip().split(";")
        game_num = numbers(header)[0]
        sprint(f"Processing game {game_num}: {rounds}")

        round_data = []
        for r in rounds:
            round_values = []
            for m in round_re.finditer(r):
                round_values.append((int(m.group(1)), m.group(2)))
            round_data.append(round_values)
        sprint(f"Round data: {round_data}")
        games.append((game_num, round_data))
    return games


def is_game_valid(game, max_cubes):
    game_id, rounds = game
    sprint(f"Checking game {game_id}")
    for round in rounds:
        sprint(f"Checking round {round}")
        for count, color in round:
            if count > max_cubes[color]:
                sprint(f"Game {game_id} is invalid. Too many {color} cubes")
                return False
    return True


def optimize_game(game):
    game_id, rounds = game
    sprint(f"Optimizing game {game_id}")
    max_cubes = {"red": 0, "green": 0, "blue": 0}
    for round in rounds:
        sprint(f"Optimizing round {round}")
        for count, color in round:
            if count > max_cubes[color]:
                max_cubes[color] = count
    return max_cubes


@print_timings
def part_1():
    data = process_input(input_data)
    sprint(f"Processed: {data}")

    valid_game = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    id_sum = 0
    for game in data:
        game_id = game[0]
        if is_game_valid(game, valid_game):
            sprint(f"Game {game_id} is valid")
            id_sum += game_id
        else:
            sprint(f"Game {game_id} is invalid")
    return id_sum


@print_timings
def part_2():
    data = process_input(input_data)

    total_power = 0
    for game in data:
        optimized = optimize_game(game)
        sprint(f"Game {game[0]} optimized: {optimized}")
        power = reduce(operator.mul, optimized.values())
        sprint(f"Game {game[0]} power: {power}")
        total_power += power
    return total_power


run(part_1, part_2)
