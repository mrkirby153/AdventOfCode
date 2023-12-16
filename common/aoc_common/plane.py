def neighbors(point: complex, diagonal=False) -> list[complex]:
    """
    Returns a list of the neighbors of the given point. If `diagonal` is True, then diagonal neighbors are included.
    `point` should be a complex number with the real part being the x coordinate and the imaginary part being the y coordinate.
    """
    points = [point + 1, point - 1, point + 1j, point - 1j]
    if diagonal:
        points.extend([point + 1 + 1j, point + 1 - 1j, point - 1 + 1j, point - 1 - 1j])
    return points


def manhattan(n1: complex, n2: complex) -> int:
    """
    Returns the manhattan distance between two points.
    """
    return int(abs(n1.real - n2.real) + abs(n1.imag - n2.imag))
