import math


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


def distance(n1: complex, n2: complex) -> float:
    """
    Returns the distance between two points.
    """
    return math.sqrt(distance_squared(n1, n2))


def distance_squared(n1: complex, n2: complex) -> float:
    """
    Returns the squared distance between two points.
    """
    return (n1.real - n2.real) ** 2 + (n1.imag - n2.imag) ** 2


def poly_area(polygon: list[complex]) -> float:
    """
    Returns the area of the given polygon using the shoelace formula. The polygon should be a list of complex numbers.

    Source: https://stackoverflow.com/a/24468019
    """
    area = 0.0
    l = len(polygon)
    for i in range(l):
        j = (i + 1) % l
        area += polygon[i].real * polygon[j].imag
        area -= polygon[j].real * polygon[i].imag
    area = abs(area) / 2.0
    return area


def perimeter(polygon: list[complex]) -> float:
    """
    Returns the perimeter of the given polygon. The polygon should be a list of complex numbers.
    """
    perimeter = 0.0
    l = len(polygon)
    for i in range(l):
        j = (i + 1) % l
        perimeter += distance(polygon[i], polygon[j])
    return perimeter


def tuple_to_complex(t: tuple) -> complex:
    """
    Converts a tuple to a complex number.

    The real part of the complex number is the first element (x) of the tuple, and the imaginary part is the second element (y).
    """
    return complex(t[0], t[1])


def complex_to_tuple(c: complex) -> tuple:
    """
    Converts a complex number to a tuple.

    The real part of the complex number is the first element (x) of the tuple, and the imaginary part is the second element (y).
    """
    return (c.real, c.imag)
