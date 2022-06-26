"""
https://fivethirtyeight.com/features/can-you-make-room-for-goats/
"""
import random
from statistics import mean
from tqdm import tqdm


def _assign_goat(occupied_floors: list[bool]) -> bool:
    """
    Make a goat pick somewhere to stay, following the rules below.
    Return true if the goat found a home,
    or false if it ended up on the roof

    Note: edits occupied floors in place!
    """
    preference = random.randint(0, len(occupied_floors) - 1)
    while preference < len(occupied_floors):
        if occupied_floors[preference]:
            preference += 1
        else:
            occupied_floors[preference] = True
            return True
    return False


def _simulate(n_floors: int = 10) -> bool:
    """
    Add goats in order to their preferred floors.
    If their preferred floor is taken,
    continue upward until there's an open floor.
    Return false if any goat ends up on the roof.
    """
    occupied_floors = [False for _ in range(n_floors)]
    for _ in range(n_floors):
        safe = _assign_goat(occupied_floors)
        if not safe:
            return False
    return True


def _main() -> float:
    # This takes ~4 minutes on my laptop
    return mean((_simulate() for _ in tqdm(range(int(1e7)))))


if __name__ == "__main__":
    print(_main())
