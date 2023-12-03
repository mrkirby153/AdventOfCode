def neigbors(point, diagonal=False):
    """
    Returns a list of the neighbors of the given point. If `diagonal` is True, then diagonal neighbors are included.
    `point` should be a complex number with the real part being the x coordinate and the imaginary part being the y coordinate.
    """
    points = [point + 1, point - 1, point + 1j, point - 1j]
    if diagonal:
        points.extend([point + 1 + 1j, point + 1 - 1j, point - 1 + 1j, point - 1 - 1j])
    return points
