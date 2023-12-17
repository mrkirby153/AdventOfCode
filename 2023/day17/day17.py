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


DIRECTION_SYMBOLS = {
    +1j: "▼",
    -1j: "▲",
    -1: "◀",
    +1: "▶",
}


def load_data(input_data):
    return as_complex_matrix_dict(to_2d_matrix(input_data))


def search(graph, start, end, max_steps, min_steps):
    frontier = PriorityQueue()

    seen = set()
    costs = {}
    prev = {}

    starts = [(start, 1, 0), (start, +1j, 0)]
    for s in starts:
        frontier.put(PrioritizedItem(0, s))
        costs[s] = 0
        prev[s] = None
    while not frontier.empty():
        current = frontier.get()
        (pos, direction, num_steps) = current.item

        if pos == end and num_steps >= min_steps:
            return current.priority, prev, current.item

        if current.item in seen:
            continue
        seen.add(current.item)

        # If we have taken less than min_steps, we can only go straight
        if num_steps < min_steps:
            new_directions = [direction]
        else:
            # If we have taken at least min_steps, we can turn
            # However, if we have taken more than max_steps, we can only turn
            if num_steps == max_steps:
                new_directions = [direction * 1j, direction * -1j]
            else:
                new_directions = [direction * 1j, direction * -1j, direction]

        for new_direction in new_directions:
            new_point = pos + new_direction
            if new_point == current:
                continue  # Cannot go back to where we came

            new_item = (
                new_point,
                new_direction,
                num_steps + 1 if new_direction == direction else 1,
            )
            cost_to_enter = costs[current.item] + int(graph.get(new_point, 1e100))
            if new_item not in costs or cost_to_enter < costs[new_item]:
                costs[new_item] = cost_to_enter
                prev[new_item] = current.item
                frontier.put(PrioritizedItem(cost_to_enter, new_item))
    return None, None, None


@print_timings
def part_1():
    graph = load_data(input_data)

    (min_x, max_x), (min_y, max_y) = get_grid_dimensions(graph)
    start = 0
    end = complex(max_x, max_y)

    cost, prev, current = search(graph, start, end, 3, 1)

    path = []
    while current is not None:
        path.append(current)
        current = prev[current]

    symbols = {k: DIRECTION_SYMBOLS[v] for (k, v, s) in path}
    path = [p[0] for p in path]

    print_matrix_dict(
        graph, sprint, lambda p, v: colorize(symbols.get(p, v), RED) if p in path else v
    )

    return cost


@print_timings
def part_2():
    graph = load_data(input_data)

    (min_x, max_x), (min_y, max_y) = get_grid_dimensions(graph)
    start = 0
    end = complex(max_x, max_y)

    cost, prev, current = search(graph, start, end, 10, 4)

    path = []
    while current is not None:
        path.append(current)
        current = prev[current]

    path = [p[0] for p in path]

    print_matrix_dict(graph, sprint, lambda p, v: colorize(v, RED) if p in path else v)

    return cost


run(part_1, part_2, __name__)

# 827 -- too low
