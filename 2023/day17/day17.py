from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import (
    as_complex_matrix_dict,
    to_2d_matrix,
    get_grid_dimensions,
    print_matrix_dict,
)
from aoc_common.search import search as aoc_search
from aoc_common.ansi import colorize, RED
from dataclasses import dataclass, field

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
    start_states = [(start, 1, 0), (start, +1j, 0)]

    def _end(state):
        return state[0] == end and state[2] >= min_steps

    def _next_states(current):
        (pos, direction, num_steps) = current

        if num_steps < min_steps:
            new_directions = [direction]  # Must go straight
        else:
            if num_steps == max_steps:
                new_directions = [direction * 1j, direction * -1j]  # Must turn
            else:
                new_directions = [direction * 1j, direction * -1j, direction]

        for new_direction in new_directions:
            new_point = pos + new_direction
            if new_point == current:
                continue  # Cannot go back to where we came

            yield (
                new_point,
                new_direction,
                num_steps + 1 if new_direction == direction else 1,
            )

    def _cost(_current_state, next_state):
        (pos, direction, num_steps) = next_state
        return int(graph.get(pos, 1e100))

    return aoc_search(start_states, _end, _next_states, _cost)


@print_timings
def part_1():
    graph = load_data(input_data)

    (min_x, max_x), (min_y, max_y) = get_grid_dimensions(graph)
    start = 0
    end = complex(max_x, max_y)

    end, path, cost = search(graph, start, end, 3, 1)
    cost = cost[end]

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

    end, path, cost = search(graph, start, end, 10, 4)
    cost = cost[end]

    path = [p[0] for p in path]

    print_matrix_dict(graph, sprint, lambda p, v: colorize(v, RED) if p in path else v)

    return cost


run(part_1, part_2, __name__)

# 827 -- too low
