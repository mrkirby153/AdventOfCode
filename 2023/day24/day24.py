from aoc_common import get_puzzle_input, run, sprint, parsed_args
from aoc_common.benchmark import print_timings
from collections import namedtuple
from aoc_common.io import numbers
from itertools import combinations
from z3 import *
from tqdm import tqdm

input_data = get_puzzle_input()

Snowflake = namedtuple("Snowflake", ["x", "y", "z", "vx", "vy", "vz"])


def load_input(input_data):
    snowflakes = []
    for line in input_data:
        pos, vel = line.split("@")
        x, y, z = numbers(pos)
        vx, vy, vz = numbers(vel)

        snowflakes.append(Snowflake(x, y, z, vx, vy, vz))
    return snowflakes


def get_collision(snowflake1, snowflake2):
    sprint(snowflake1, snowflake2)
    s = Solver()
    t = Real("t")
    t2 = Real("t2")
    eq1 = snowflake1.x + snowflake1.vx * t == snowflake2.x + snowflake2.vx * t2
    eq2 = snowflake1.y + snowflake1.vy * t == snowflake2.y + snowflake2.vy * t2
    s.add(eq1, eq2)
    s.add(t > 0, t2 > 0)  # Collision must happen in the future

    if s.check() != sat:
        sprint("no collision")
        return None, None  # No collision

    model = s.model()
    sprint(model)

    t1 = float(model[t].as_decimal(10).replace("?", ""))

    posx = snowflake1.x + (snowflake1.vx * t1)
    posy = snowflake1.y + (snowflake1.vy * t1)
    sprint("Collision at", posx, posy)
    return (posx, posy)


def collide_in_test_area(snowflake1, snowflake2, x_range, y_range):
    posx, posy = get_collision(snowflake1, snowflake2)
    if posx is None:
        return False
    return (
        x_range.start <= posx <= x_range.stop and y_range.start <= posy <= y_range.stop
    )


@print_timings
def part_1():
    snowflakes = load_input(input_data)

    x_range = (
        range(7, 27) if parsed_args.sample else range(200000000000000, 400000000000000)
    )
    y_range = (
        range(7, 27) if parsed_args.sample else range(200000000000000, 400000000000000)
    )

    count = 0
    for snowflake1, snowflake2 in tqdm(combinations(snowflakes, 2)):
        if collide_in_test_area(snowflake1, snowflake2, x_range, y_range):
            count += 1
    return count


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)
