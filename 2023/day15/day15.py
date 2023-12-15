from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from collections import defaultdict
import re

input_data = get_puzzle_input()


instruction_re = re.compile(r"(\w+)([-=])(\d+)?")


def do_hash(string):
    curr = 0
    for char in string:
        curr += ord(char)
        curr *= 17
        curr %= 256
    return curr


@print_timings
def part_1():
    total = 0
    for seq in input_data[0].split(","):
        sprint(seq, do_hash(seq))
        total += do_hash(seq)
    return total


@print_timings
def part_2():
    boxes = defaultdict(list)

    def _print_boxes():
        for k, v in boxes.items():
            sprint("Box ", k, v)

    def _get_index(box, lens):
        sprint("Looking for", lens, "in", box)
        for i, (existing_lens, length) in enumerate(box):
            if lens == existing_lens:
                return i
        return None

    for instruction in input_data[0].split(","):
        sprint()
        sprint("Executing", instruction)

        match = instruction_re.match(instruction)

        lens = match.group(1)
        ins = match.group(2)

        box_num = do_hash(lens)
        sprint("Mutating box", box_num)
        box = boxes[box_num]

        if ins == "=":
            focal_length = int(match.group(3))
            index = _get_index(box, lens)
            sprint("Setting", index, "to", focal_length, "in", box)
            if index is None:
                box.append((lens, focal_length))
            else:
                box[index] = (lens, focal_length)
        elif ins == "-":
            index = _get_index(box, lens)
            sprint("Removing", index, "from", box)
            if index is not None:
                del box[index]
        else:
            assert False, f"Unknown instruction {ins}"

        sprint("After", instruction)
        _print_boxes()

    total = 0
    for box_num, box_contents in boxes.items():
        for lens_num, (lens, power) in enumerate(box_contents):
            lens_power = (box_num + 1) * (lens_num + 1) * power
            sprint("Lens", lens, "has power", power)
            total += lens_power
    return total


run(part_1, part_2, __name__)
