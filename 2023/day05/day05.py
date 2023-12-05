from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import numbers
from aoc_common.ansi import colorize, RED
from collections import deque

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
        # sprint("Processing line", line)
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


def expand_seeds(seeds):
    ranges = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        amount = seeds[i + 1]
        ranges.append(range(start, start + amount))
    return ranges


def partially_contained(range_one, range_two):
    x1, x2 = range_one.start, range_one.stop
    y1, y2 = range_two.start, range_two.stop
    return x1 <= y2 and y1 <= x2


def map_range(mapping, candidate_range):
    sprint("Mapping", candidate_range, "against", mapping)
    dest = mapping[0]
    start = mapping[1]
    size = mapping[2]
    stop = start + size - 1

    offset = start - dest
    if not partially_contained(
        candidate_range, range(start, stop)
    ) and not partially_contained(range(start, stop), candidate_range):
        sprint("Ranges do not overlap")
        return None, None
    if candidate_range.start >= start and candidate_range.stop <= stop:
        # The range is completely within this mapping
        sprint("Range is completely within this mapping")
        return (
            range(candidate_range.start - offset, candidate_range.stop - offset),
            None,
        )
    elif candidate_range.start >= start and candidate_range.stop >= stop:
        # The range starts within this mapping and ends after it. Split the range into two ranges
        result = (
            range(candidate_range.start - offset, stop - offset + 1),
            range(stop + 1, candidate_range.stop),
        )
        sprint("Range starts within this mapping and ends after it, mapped to", result)
        return result
    elif candidate_range.start <= start and candidate_range.stop <= stop:
        # The range starts before the mapping and ends within it. Split the range into two ranges
        result = (
            range(start - offset, candidate_range.stop - offset),
            range(candidate_range.start, start - 1),
        )
        sprint("Range starts before the mapping and ends within it, mapped to", result)
        return result
    else:
        # The range does not overlap with this mapping. Just return the range as-is
        sprint("Range does not overlap with this mapping")
        return None, None


def do_mapping(mappings, candidate_range):
    queue = deque([candidate_range])
    mapped_ranges = []

    while queue:
        to_process = queue.popleft()
        sprint("Processing", to_process)
        found = False
        for mapping in mappings:
            new_range, unprocessed = map_range(mapping, to_process)
            if new_range:
                found = True
                sprint("Mapped", to_process, "to", new_range)
                mapped_ranges.append(new_range)
            if unprocessed:
                sprint("Unprocessed:", unprocessed)
                queue.append(unprocessed)
        if not found:
            sprint("Processed range and found no mappings")
            mapped_ranges.append(to_process)
    return mapped_ranges


@print_timings
def part_2():
    seeds, locations = load_input(input_data)
    sprint("Seeds:", locations)

    ranges = expand_seeds(seeds)

    for mapping in [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]:
        lookup_table = locations[mapping]
        new_ranges = []
        for r in ranges:
            new_ranges.extend(do_mapping(lookup_table, r))
        print(new_ranges, mapping)
        ranges = new_ranges
    return min(map(lambda x: x.start, ranges))


run(part_1, part_2)
