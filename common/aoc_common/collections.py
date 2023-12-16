from typing import Any, Generator, Iterable, TypeVar

T = TypeVar("T")


def chunk(iterator: Iterable[T], size) -> Generator[list[T]]:
    """
    Chunks an iterator into the given size
    """
    iterator = iter(iterator)
    should_run = True
    while should_run:
        chunk = []
        for _ in range(size):
            try:
                next_val = next(iterator)
                chunk.append(next_val)
            except StopIteration:
                should_run = False
                break
        if chunk:
            yield chunk
