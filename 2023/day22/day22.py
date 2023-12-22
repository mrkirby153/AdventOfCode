from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from collections import namedtuple
from tqdm import tqdm

input_data = get_puzzle_input()

Point = namedtuple("Point", ["x", "y", "z"])
Brick = namedtuple("Brick", ["a", "b"])


def inside(point, brick):
    return (
        brick.a.x <= point.x <= brick.b.x
        and brick.a.y <= point.y <= brick.b.y
        and brick.a.z <= point.z <= brick.b.z
    )


def intersect(brick1, brick2):
    return (
        brick1.a.x <= brick2.b.x
        and brick1.b.x >= brick2.a.x
        and brick1.a.y <= brick2.b.y
        and brick1.b.y >= brick2.a.y
        and brick1.a.z <= brick2.b.z
        and brick1.b.z >= brick2.a.z
    )


def load_input(data):
    bricks = []
    for line in data:
        start, end = line.split("~")
        start = Point(*map(int, start.split(",")))
        end = Point(*map(int, end.split(",")))
        bricks.append(Brick(start, end))
    return bricks


def print_1(data, max_x, max_y, max_z):
    # Print the bricks X and Z axis
    sprint("".join(["X" if x == ((max_x + 1) // 2) else " " for x in range(max_x + 1)]))
    sprint("".join([str(x) for x in range(max_x + 1)]))
    for z in range(max_z, -1, -1):
        for x in range(max_x + 1):
            if z == 0:
                sprint("-", end="")
                continue
            for brick in data:
                is_inside = [inside(Point(x, y, z), brick) for y in range(max_y + 1)]

                if any(is_inside):
                    sprint("#", end="")
                    break
            else:
                sprint(".", end="")
        sprint(f" {z}", end="")
        if z == ((max_z + 1) // 2):
            sprint(" Z", end="\n")
        else:
            sprint("", end="\n")


def print_2(data, max_x, max_y, max_z):
    sprint("".join(["X" if x == ((max_y + 1) // 2) else " " for x in range(max_y + 1)]))
    sprint("".join([str(y) for y in range(max_y + 1)]))
    for z in range(max_z, -1, -1):
        for y in range(max_y + 1):
            if z == 0:
                sprint("-", end="")
                continue
            for brick in data:
                is_inside = [inside(Point(x, y, z), brick) for x in range(max_x + 1)]

                if any(is_inside):
                    sprint("#", end="")
                    break
            else:
                sprint(".", end="")
        sprint(f" {z}", end="")
        if z == ((max_z + 1) // 2):
            sprint(" Z", end="\n")
        else:
            sprint("", end="\n")


def find_max_z(data):
    return max([brick.b.z for brick in data] + [brick.a.z for brick in data])


def fall_bricks(bricks):
    bricks = bricks.copy()
    # Move all of the bricks down as far as they can go without intersecting with another brick
    max_z = find_max_z(bricks)
    settled_bricks = []
    sprint(f"Max Z: {max_z}")
    for z in tqdm(range(1, max_z + 1), desc="falling bricks"):
        candidates = []
        for brick in bricks:
            if brick.a.z == z or brick.b.z == z:
                candidates.append(brick)
        sprint(f"processing layer {z}, candidates: {candidates}")
        for brick in candidates:
            # Move the brick down as far as it can go
            new_brick = Brick(
                Point(brick.a.x, brick.a.y, brick.a.z),
                Point(brick.b.x, brick.b.y, brick.b.z),
            )
            # Remove the brick from the list of bricks
            bricks.remove(brick)
            while min(new_brick.a.z, new_brick.b.z) > 1:
                new_brick = Brick(
                    Point(new_brick.a.x, new_brick.a.y, new_brick.a.z - 1),
                    Point(new_brick.b.x, new_brick.b.y, new_brick.b.z - 1),
                )
                if any([intersect(new_brick, settled) for settled in settled_bricks]):
                    new_brick = Brick(
                        Point(new_brick.a.x, new_brick.a.y, new_brick.a.z + 1),
                        Point(new_brick.b.x, new_brick.b.y, new_brick.b.z + 1),
                    )
                    break
            settled_bricks.append(new_brick)
    return settled_bricks


def can_tower_fall(bricks):
    initial = sorted(bricks)
    final = sorted(fall_bricks(bricks))
    return initial != final


def determine_bricks_to_remove(settled_bricks):
    # A brick can be removed if it is not supporting any other bricks
    bricks_to_remove = []
    for brick in tqdm(settled_bricks, desc="determining bricks to remove"):
        new_bricks = settled_bricks.copy()
        new_bricks.remove(brick)
        if not can_tower_fall(new_bricks):
            bricks_to_remove.append(brick)
    return bricks_to_remove


@print_timings
def part_1():
    data = load_input(input_data)
    new_bricks = fall_bricks(data)
    return len(determine_bricks_to_remove(new_bricks))


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)
