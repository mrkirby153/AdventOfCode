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


def get_collision(snowflake1, snowflake2, min_pos, max_pos):
    sprint(snowflake1, snowflake2)
    s = Solver()
    t = Real("t")
    t2 = Real("t2")
    eq1 = snowflake1.x + snowflake1.vx * t == snowflake2.x + snowflake2.vx * t2
    eq2 = snowflake1.y + snowflake1.vy * t == snowflake2.y + snowflake2.vy * t2
    s.add(eq1, eq2)
    s.add(t >= 0, t2 >= 0)  # Collision must happen in the future
    s.add(min_pos <= (snowflake1.x + snowflake1.vx * t))
    s.add(max_pos >= (snowflake1.x + snowflake1.vx * t))
    s.add(min_pos <= (snowflake1.y + snowflake1.vy * t))
    s.add(max_pos >= (snowflake1.y + snowflake1.vy * t))
    return s.check() == sat


@print_timings
def part_1():
    snowflakes = load_input(input_data)

    min_pos, max_pos = (
        (7, 27) if parsed_args.sample else (200000000000000, 400000000000000)
    )

    count = 0
    for i in tqdm(range(len(snowflakes)), desc="One"):
        for j in tqdm(range(i + 1, len(snowflakes)), desc="Two"):
            if get_collision(snowflakes[i], snowflakes[j], min_pos, max_pos):
                count += 1
    return count


@print_timings
def part_2():
    snowflakes = load_input(input_data)

    s = Solver()

    rock_vel_x = Real("rock_vel_x")
    rock_vel_y = Real("rock_vel_y")
    rock_vel_z = Real("rock_vel_z")

    rock_pos_x = Real("rock_pos_x")
    rock_pos_y = Real("rock_pos_y")
    rock_pos_z = Real("rock_pos_z")

    # We want to find the velocity and position of the rock that will collide with all the snowflakes
    for i, snowflake in enumerate(snowflakes):
        t = Real(f"t{i}")
        s.add(t >= 0)
        s.add(rock_pos_x + rock_vel_x * t == snowflake.x + snowflake.vx * t)
        s.add(rock_pos_y + rock_vel_y * t == snowflake.y + snowflake.vy * t)
        s.add(rock_pos_z + rock_vel_z * t == snowflake.z + snowflake.vz * t)
    assert s.check() == sat

    model = s.model()
    print("x", model.evaluate(rock_pos_x))
    print("y", model.evaluate(rock_pos_y))
    print("z", model.evaluate(rock_pos_z))
    return sum(
        int(str(model.evaluate(pos))) for pos in [rock_pos_x, rock_pos_y, rock_pos_z]
    )


run(part_1, part_2, __name__)
