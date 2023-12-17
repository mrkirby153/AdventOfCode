from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import (
    as_complex_matrix_dict,
    to_2d_matrix,
    get_grid_dimensions,
    print_matrix_dict,
)
from aoc_common.plane import manhattan
from aoc_common.ansi import colorize, RED
from dataclasses import dataclass, field
from queue import PriorityQueue

input_data = get_puzzle_input()


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: any = field(compare=False)


DIRECTIONS = {
    1: 0 + 1j,  # Up
    2: 0 - 1j,  # Down
    3: -1 + 0j,  # Left
    4: 1 + 0j,  # Right
}


def to_direction(ordinal):
    return DIRECTIONS[ordinal]


def from_direction(direction):
    return DIRECTIONS.index(direction)


def load_data(input_data):
    return as_complex_matrix_dict(to_2d_matrix(input_data))


def from_complex(c):
    return int(c.real), int(c.imag)


def to_complex(x):
    return complex(x[0], x[1])


def a_star(graph, start, end, max_steps):
    frontier = PriorityQueue()

    starts = [PrioritizedItem(0, (start, 1, 0)), PrioritizedItem(0, (start, -1j, 0))]

    came_from = {}
    costs = {}

    for s in starts:
        frontier.put(s)
        came_from[s.item[0]] = None
        costs[s.item[0]] = 0

    while not frontier.empty():
        sprint("---")
        current = frontier.get()

        (point, direction, num_steps) = current.item
        sprint("Current", point, direction, num_steps)

        assert num_steps <= max_steps, f"Too many steps, {num_steps}"

        if point == end:
            break

        candidate_directions = []
        candidate_directions.extend(
            [direction * 1j, direction * -1j]
        )  # Turn left or right
        if num_steps < max_steps:
            candidate_directions.append(direction)  # Go straight
        else:
            sprint("Must turn")

        sprint("Candidate directions", candidate_directions)
        for new_direction in candidate_directions:
            new_point = point + new_direction

            if new_point not in graph:
                continue  # This point is out of bounds
            if graph[new_point] == ".":  # This is a wall
                continue

            new_cost = costs[point] + int(graph[new_point])
            if new_point not in costs or new_cost < costs[new_point]:
                sprint("Adding to frontier", new_point, "with cost", new_cost)
                costs[new_point] = new_cost
                priority = new_cost + manhattan(new_point, end)
                frontier.put(
                    PrioritizedItem(
                        priority,
                        (
                            new_point,
                            new_direction,
                            num_steps + 1 if new_direction == direction else 0,
                        ),
                    )
                )
                came_from[new_point] = point
    return came_from, costs


@print_timings
def part_1():
    graph = load_data(input_data)

    (min_x, max_x), (min_y, max_y) = get_grid_dimensions(graph)
    start = 0
    end = complex(max_x, max_y)

    came_from, cost = a_star(graph, start, end, 3)
    marked_points = []

    current = end
    while current != start:
        marked_points.append(current)
        current = came_from[current]

    print_matrix_dict(
        graph,
        sprint,
        lambda p, v: colorize(str(v), RED) if p in marked_points else v,
    )
    return cost[end]


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)

# 673 -- Too low
