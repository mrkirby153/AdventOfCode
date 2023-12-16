from queue import PriorityQueue
from typing import Callable, Iterable, List, TypeVar

T = TypeVar("T")


def _trace(parents, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parents[path[-1]])
    path.reverse()
    return path


def bfs(
    start_state: T,
    end_condition: Callable[[T], bool],
    next_states: Callable[[T], Iterable[T]],
    trace=False,
):
    """
    Generic BFS.

    :param start_state: The starting state
    :param end_condition: A function that returns True if the state is the end state
    :param next_states: A function that returns the next states from the current state
    """
    queue = [start_state]
    seen = set()
    parents = {}

    while queue:
        state = queue.pop(0)
        if end_condition(state):
            return state if not trace else _trace(parents, start_state, state)

        if state in seen:
            continue

        seen.add(state)
        if not trace:
            queue.extend(next_states(state))
        else:
            for next_state in next_states(state):
                if next_state not in queue:
                    queue.append(next_state)
                    parents[next_state] = state


def dijkstra(
    starts: List[T],
    neighbors: Callable[[T], Iterable[T]],
    cost: Callable[[T, T], int] = None,
):
    """
    Generic Dijkstra's algorithm.

    :param starts: The starting states
    :param neighbors: A function that returns the neighbors of a state
    :param cost: A function that returns the cost of moving from one state to another

    :return: A tuple of (came_from, costs) where came_from is a dict of state -> previous state and costs is a dict of state -> cost
    """
    if not isinstance(starts, list):
        starts = [starts]

    if cost is None:
        cost = lambda current, next: 1

    frontier = PriorityQueue()

    came_from = {}
    costs = {}
    for start in starts:
        frontier.put(start, 0)
        came_from[start] = None
        costs[start] = 0

    while not frontier.empty():
        current = frontier.get()
        for neighbor in neighbors(current):
            new_cost = costs[current] + cost(current, neighbor)
            if current not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                frontier.put(neighbor, new_cost)
                came_from[neighbor] = current
    return came_from, costs


def a_star(
    starts: List[T],
    goal: T,
    neighbors: Callable[[T], Iterable[T]],
    cost: Callable[[T, T], int] = None,
    herustic: Callable[[T, T], int] = None,
):
    """
    Generic A* algorithm.

    :param starts: The starting states
    :param goal: The goal state
    :param neighbors: A function that returns the neighbors of a state
    :param cost: A function that returns the cost of moving from one state to another
    :param herustic: A function that returns the herustic cost of moving from one state to another

    :return: A tuple of (came_from, costs) where came_from is a dict of state -> previous state and costs is a dict of state -> cost
    """
    if not isinstance(starts, list):
        starts = [starts]

    if cost is None:
        cost = lambda current, next: 1
    if herustic is None:
        herustic = lambda a, b: sum(abs(x - y) for x, y in zip(a, b))

    frontier = PriorityQueue()

    came_from = {}
    costs = {}
    for start in starts:
        frontier.put(start, 0)
        came_from[start] = None
        costs[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        for neighbor in neighbors(current):
            new_cost = costs[current] + cost(current, neighbor)
            if current not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                priority = new_cost + herustic(neighbor, goal)
                frontier.put(neighbor, priority)
                came_from[neighbor] = current
    return came_from, costs
