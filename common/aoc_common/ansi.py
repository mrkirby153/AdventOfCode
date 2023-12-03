BLACK = "\033[90m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

RESET = "\033[0m"

_ALL = [BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, WHITE, RESET, "", None]


def colorize(text, color):
    """
    Colorizes the given text with the given color
    """
    assert color in _ALL, f"Invalid color: {color}"
    return f"{color}{text}{RESET}"
