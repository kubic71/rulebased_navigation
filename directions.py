all_directions = list([
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1)])

directions_map = {
    (1, 0): "→",
    (1, 1): "↘",
    (0, 1): "↓",
    (-1, 1): "↙",
    (-1, 0): "←",
    (-1, -1): "↖",
    (0, -1): "↑",
    (1, -1): "↗",
}


def rotate(direction, clockwise=True):
    # only applicable to (dx, dy) direction vectors of the rover
    dir_index = (all_directions.index(direction) + (1 if clockwise else -1)) % len(all_directions)
    return all_directions[dir_index]