from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import numbers
from aoc_common.ansi import colorize, RED

input_data = get_puzzle_input()


def load_input(input_data):
    locations = {
        "seed-to-soil": [],
        "soil-to-fertilizer": [],
        "fertilizer-to-water": [],
        "water-to-light": [],
        "light-to-temperature": [],
        "temperature-to-humidity": [],
        "humidity-to-location": [],
    }
    seeds = numbers(input_data[0])

    current_loc = None
    for line in input_data[1:]:
        sprint("Processing line", line)
        if line.endswith("map:"):
            current_loc = locations[line.split()[0]]
            assert current_loc is not None, f"No location found for {current_loc}"
            continue
        mapping = numbers(line)
        if len(mapping) > 0:
            assert current_loc is not None, f"No location found"
            current_loc.append(mapping)
    return seeds, locations


def get_target_range(ranges, number):
    for r in ranges:
        start = r[1]
        if number >= start and number <= start + r[2]:
            return r
    return None


def translate(destination_start, source_start, size, source):
    sprint(
        "Translating",
        source,
        "from",
        source_start,
        "to",
        destination_start,
        "with size",
        size,
    )
    if source > source_start + size - 1:
        sprint("not in range")
        return source

    offset = source_start - destination_start
    sprint("Source offset:", offset)
    return source - offset


def map_seed(lookup_table, seed_num):
    target_range = get_target_range(lookup_table, seed_num)
    if target_range:
        return translate(target_range[0], target_range[1], target_range[2], seed_num)
    else:
        return seed_num


@print_timings
def part_1():
    seeds, locations = load_input(input_data)
    sprint("Seeds:", seeds)
    sprint("Locations:", locations)

    for mapping in [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]:
        sprint("Mapping", mapping)
        lookup_table = locations[mapping]
        for i in range(len(seeds)):
            start = seeds[i]
            dest = map_seed(lookup_table, start)
            sprint(colorize(f"Seed {start} maps to {dest}", RED))
            seeds[i] = dest
    return min(seeds)


@print_timings
def part_2():
    pass


run(part_1, part_2)
