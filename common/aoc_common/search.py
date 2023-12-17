from queue import PriorityQueue
from typing import Callable, Iterable, List, TypeVar, Generic

from dataclasses import dataclass, field

T = TypeVar("T")


@dataclass(order=True)
class PrioritizedItem(Generic[T]):
    priority: int
    item: T = field(compare=False)


def _trace(parents, start):
    path = []
    current = start

    while current is not None:
        path.append(current)
        current = parents[current]
    return list(reversed(path))


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
            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                frontier.put(neighbor, new_cost)
                came_from[neighbor] = current
    return came_from, costs


def search(
    start_states: Iterable[T],
    end_condition: Callable[[T], bool],
    next_states: Callable[[T], Iterable[T]],
    cost: Callable[[T, T], int] = None,
    herustic: Callable[[T], int] = None,
):
    """
    A generic search algorithm that uses A* if `herustic` is not None, otherwise uses Dijkstra's algorithm.

    If cost is 1, this is equivalent to BFS.

    :param start_states: The starting states
    :param end_condition: A function that returns True if the state is the end state
    :param next_states: A function that returns the next states from the current state
    :param cost: A function that returns the cost of moving from one state to another
    :param herustic: A function that returns the herustic cost of moving from one state towards the goal state

    :return: A three tuple of (end_state, path, costs) where end_state is the end state, path is a list of states from the start state to the end state, and costs is a dict of state -> cost
    """

    frontier = PriorityQueue[PrioritizedItem[T]]()

    costs = {}
    prev = {}

    for start in start_states:
        frontier.put(PrioritizedItem(0, start))
        costs[start] = 0
        prev[start] = None

    while not frontier.empty():
        current = frontier.get().item

        if end_condition(current):
            return current, _trace(prev, current), costs

        for next_state in next_states(current):
            next_cost = costs[current] + cost(current, next_state)
            if next_state not in costs or next_cost < costs[next_state]:
                costs[next_state] = next_cost
                priority = next_cost + herustic(next_state) if herustic else next_cost
                prev[next_state] = current
                frontier.put(PrioritizedItem(priority, next_state))
    return None, None, costs
