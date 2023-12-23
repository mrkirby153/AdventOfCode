from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from aoc_common.io import (
    as_complex_matrix_dict,
    to_2d_matrix,
    get_grid_dimensions,
    print_matrix_dict,
)
from aoc_common.plane import neighbors as plane_neighbors
from aoc_common.ansi import colorize, RED
from collections import deque
from collections import defaultdict
from tqdm import tqdm

input_data = get_puzzle_input()

DOWNHILL_DIRECTIONS = {
    ">": 1,
    "<": -1,
    "V:": 1j,
}


def load_input(input_data):
    return as_complex_matrix_dict(to_2d_matrix(input_data))


def find_start(grid):
    (min_x, max_x), (min_y, max_y) = get_grid_dimensions(grid)
    for x in range(max_x + 1):
        if grid[complex(x, 0)] == ".":
            return complex(x, 0)


def find_end(grid):
    (min_x, max_x), (min_y, max_y) = get_grid_dimensions(grid)
    for x in range(max_x + 1):
        if grid[complex(x, max_y)] == ".":
            return complex(x, max_y)


def neighbors(grid, pos, slopes=True):
    if slopes:
        if grid[pos] == "v":
            yield pos + 1j
            return
        elif grid[pos] == "^":
            yield pos - 1j
            return
        elif grid[pos] == ">":
            yield pos + 1
            return
        elif grid[pos] == "<":
            yield pos - 1
            return

    for n in plane_neighbors(pos):
        if n in grid and grid[n] != "#":
            yield n


def find_longest_path(grid, start, end):
    queue = deque([(start, set())])
    costs = dict()
    costs[start] = 0
    while queue:
        print("queue", len(queue), end="\r")
        pos, path = queue.pop()
        if pos == end:
            continue
        for n in neighbors(grid, pos):
            new_cost = costs[pos] + 1
            if n in path:
                continue  # already visited
            if n not in costs or new_cost > costs[n]:
                costs[n] = new_cost
                new_path = path.copy()
                new_path.add(n)
                queue.appendleft((n, new_path))
    return costs[end]


def get_vertexes(grid):
    vertexes = []
    for pos, val in grid.items():
        if val == "#":
            continue
        adjacent = [
            grid[n] for n in plane_neighbors(pos) if n in grid and grid[n] != "#"
        ]
        if len(adjacent) > 2:
            vertexes.append(pos)
    return vertexes


def connect_vertexes(grid, vertexes):
    connections = defaultdict(lambda: list())
    for v in tqdm(vertexes):
        queue = []
        queue.append(v)
        seen = {v}
        dist = 0
        while queue:
            nq = []
            dist += 1
            for c in queue:
                for a in neighbors(grid, c, False):
                    if a not in seen:
                        if a in vertexes:
                            connections[v].append((dist, a))
                            seen.add(a)
                        else:
                            seen.add(a)
                            nq.append(a)
            queue = nq
    return connections


@print_timings
def part_1():
    grid = load_input(input_data)
    start = find_start(grid)
    end = find_end(grid)
    return find_longest_path(grid, start, end)


@print_timings
def part_2():
    grid = load_input(input_data)
    start = find_start(grid)
    end = find_end(grid)
    vertexes = get_vertexes(grid)
    vertexes.append(start)
    vertexes.append(end)

    graph = connect_vertexes(grid, vertexes)

    print_matrix_dict(
        grid, sprint, lambda k, v: colorize(v, RED if k in vertexes else "")
    )

    best = 0

    def dfs(cur, seen=None, total=0):
        if seen is None:
            seen = set()
        nonlocal best
        if cur == end:
            if total > best:
                print("new best", total)
                best = total
            return
        for distance, node in graph[cur]:
            if node not in seen:
                dfs(node, seen | {node}, total + distance)

    dfs(start)
    return best


run(part_1, part_2, __name__)
