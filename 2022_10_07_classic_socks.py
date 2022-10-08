"""
https://fivethirtyeight.com/features/can-you-fold-all-your-socks/
"""
import random
from statistics import mean
from typing import Set
from tqdm import tqdm


def _get_socks(n_pairs: int) -> list[int]:
    return list(range(n_pairs)) + list(range(n_pairs))


def _fold_socks(socks: list[int], spaces_on_chair: int) -> bool:
    chair: Set[int] = set()
    for sock in socks:
        if sock in chair:
            chair.remove(sock)
        else:
            chair.add(sock)
        if len(chair) > spaces_on_chair:
            return False
    return True


def _shuffle(socks: list[int]) -> list[int]:
    return random.sample(socks, k=len(socks))


def main(
    pairs_of_socks: int = 14,
    spaces_on_chair: int = 9,
    # This took around 5 minutes on my laptop
    iterations: int = int(1e6),
):
    socks = _get_socks(pairs_of_socks)
    successes = [
        _fold_socks(_shuffle(socks), spaces_on_chair) for _ in tqdm(range(iterations))
    ]
    print(mean(successes))


if __name__ == "__main__":
    main()
