from typing import Any, Callable

def bfs(start_state: Any, end_condition: Callable[[Any], bool], next_states: Callable[[Any], list], status: bool = False):
    """
    Generic BFS
    """
    queue = [start_state]
    seen = set()

    while queue:
        state = queue.pop(0)
        if end_condition(state):
            return state
        
        if state in seen:
            continue
        
        seen.add(state)
        queue.extend(next_states(state))