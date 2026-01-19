import random
from typing import Tuple


def roll(number: int, sides: int) -> int:
    """Rolls a specified number of dice with a certain number of sides (e.g., 3d6)."""
    return sum(random.randint(1, sides) for _ in range(number))


def d20() -> int:
    """Standard d20 roll for checks."""
    return random.randint(1, 20)


def d20_advantage() -> int:
    """Roll 2d20 and take the better result[cite: 230]."""
    return max(random.randint(1, 20), random.randint(1, 20))


def d20_disadvantage() -> int:
    """Roll 2d20 and take the lesser result[cite: 231]."""
    return min(random.randint(1, 20), random.randint(1, 20))


def ftd_attribute() -> int:
    """Standard 3d6 for human attributes[cite: 298]."""
    return roll(3, 6)