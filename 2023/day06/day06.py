from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import numbers
from tqdm import tqdm
from operator import mul
from functools import reduce

input_data = get_puzzle_input()


def load_input(input_data):
    times = []
    records = []
    times = numbers(input_data[0])
    records = numbers(input_data[1])
    return times, records


def load_input_2(input_data):
    time = int("".join(map(str, numbers(input_data[0]))))
    record = int("".join(map(str, numbers(input_data[1]))))
    return time, record


def calculate_distance(hold_time, total_time):
    remaining_time = total_time - hold_time
    sprint(
        "Hold time:",
        hold_time,
        "Remaining time:",
        remaining_time,
        "Distance:",
        remaining_time * hold_time,
    )
    return remaining_time * hold_time


def can_win(hold_time, total_time, record):
    win = calculate_distance(hold_time, total_time) > record
    sprint("Win:", win)
    return win


def get_winning_hold_times(total_time, record):
    winning_times = []
    for hold_time in tqdm(range(total_time + 1)):
        if can_win(hold_time, total_time, record):
            winning_times.append(hold_time)
    return winning_times


@print_timings
def part_1():
    winning_times = []
    times, records = load_input(input_data)
    for i in tqdm(range(len(times))):
        time = times[i]
        record = records[i]
        sprint("Time:", time, "Record:", record)
        results = get_winning_hold_times(time, record)
        sprint("Winning times:", results, "Total:", len(results))
        winning_times.append(len(results))
    return reduce(mul, winning_times)


@print_timings
def part_2():
    time, record = load_input_2(input_data)
    sprint("Time:", time, "Record:", record)
    results = get_winning_hold_times(time, record)
    return len(results)


run(part_1, part_2)
