from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import numbers

input_data = get_puzzle_input()


def load_data(input_data):
    data = []
    for line in input_data:
        springs, key = line.split(" ")
        key = numbers(key)
        data.append((springs, key))
    return data


# Springs - The map of springs
# Key - The key to the springs
# num_matched - The number of springs that have been matched in this sequence. None if nothing has been matched yet
def determine_combinations(springs, key, num_matched=0):
    if len(springs) == 0:
        # We have reached the end of the springs or the key. If we have matched all the springs, this is valid
        sprint("Ran out of springs or key", springs, key)
        return 1 if len(key) == 0 else 0

    candidate_spring = springs[0]
    print(
        "Checking",
        candidate_spring,
        "num matched",
        num_matched,
    )

    def _working():
        print("Working")
        nonlocal springs, key, num_matched
        # The current spring is working. Move to the next spring
        return determine_combinations(springs[1:], key, num_matched)

    def _broken():
        print("broken")
        nonlocal springs, key, num_matched

        if len(key) == 0:
            return 0  # We have run out of keys, but there are still springs to check
        current_key = key[0]
        # The current spring is broken. Increment the number of matched springs and try the next spring
        num_matched += 1
        print("incremented num_matched", num_matched, current_key)

        # If we have matched all the springs in our key, reset the number of matched, move two (since there will always be a working spring after a series of broken ones)
        if num_matched == current_key:
            print("num_matched == current_key")
            # Check if the next spring is working or unknown
            if springs[1] in ".?":
                return determine_combinations(springs[2:], key[1:], 0)
            else:
                return 0
        else:
            if num_matched > current_key:
                # This is not a valid combination, because we have too many broken springs
                print("Invalid, num_matched > current_key")
                return 0
            else:
                print("Checking next spring")
                # Check the next spring
                return determine_combinations(springs[1:], key, num_matched)

    if candidate_spring == ".":
        return _working()
    elif candidate_spring == "#":
        return _broken()
    elif candidate_spring == "?":
        # This spring can either be broken or working. We need to try both
        return _working() + _broken()

    else:
        assert False, f"Unknown type {candidate_spring}"


@print_timings
def part_1():
    data = load_data(input_data)

    # result = {}
    # for i, (springs, key) in enumerate(data):
    #     springs = springs + "."
    #     result[springs] = determine_combinations(springs, key)
    #     # print(determine_combinations(springs, key))

    # for k, v in result.items():
    #     print(k, v)

    # springs2, key = "?#?#?#?#?#?#?#?", [1, 3, 1, 6]
    springs, key = "?###????????" + ".", [3, 2, 1]

    return determine_combinations(springs, key)


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)
