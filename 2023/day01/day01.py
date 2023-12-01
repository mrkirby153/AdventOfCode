from aoc_common import get_puzzle_input, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import numbers

input_data = get_puzzle_input()

num_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def extract_first_and_last_numbers(line):
    processed = numbers(line, single=True)
    num = int(f"{processed[0]}{processed[-1]}")
    sprint(f"{line} -> {processed} -> {num}")
    return num


def get_number(string):
    if string[0] >= "0" and string[0] <= "9":
        return int(string[0])
    else:
        for num in num_map:
            if string.startswith(num):
                return num_map[num]
    return None


def extract_first_and_last_numbers_text(line):
    first_num = None
    last_num = None

    first_num = None
    last_num = None
    for i in range(len(line)):
        candidate = line[i:]
        sprint(f"candidate: {candidate}")
        num = get_number(candidate)
        if num is not None:
            if first_num is None:
                sprint(f"It is the first number")
                first_num = num
            last_num = num
            sprint(f"Found number {num}")
    sprint(f"!! {first_num} {last_num}")
    return int(f"{first_num}{last_num}")


@print_timings
def part_1():
    acc = 0
    for line in input_data:
        acc += extract_first_and_last_numbers(line)
    return acc


@print_timings
def part_2():
    acc = 0
    for line in input_data:
        sprint("----")
        found_num = extract_first_and_last_numbers_text(line)
        sprint(f"Found number: {found_num}")
        acc += found_num
    return acc


print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")
