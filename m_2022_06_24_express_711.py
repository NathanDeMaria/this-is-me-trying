"""
https://fivethirtyeight.com/features/can-you-make-room-for-goats/
"""
from itertools import product
from math import prod
from typing import Iterable


def _get_sum_combinations(
    factors: list[int], n_addends: int = 4
) -> Iterable[tuple[int, list[int]]]:
    """
    Find all different #s we can sum to with different combinations
    of these factors into 4 values
    """
    assignments = product(*(range(n_addends) for _ in factors))
    for assignment in assignments:
        addends = [1 for _ in range(n_addends)]
        # This is super inefficient. Could be sped up by:
        # - removing duplicates (since factors aren't unique)
        # - immediately dropping anything with an addend above 7.11
        for factor, index in zip(factors, assignment):
            addends[index] *= factor
        yield sum(addends), addends


def _main():
    # Prime factors of 711, dividing 79 by 100
    # because it 79 and 7.9 immediately take us over $7.11
    factors = [3, 3, 0.79]
    target = prod(factors)
    while True:
        for total, items in _get_sum_combinations(factors):
            error = abs(total - target)
            if error < 0.001:
                return items
        # Adding in these factors is the only way to keep the product the same
        factors.extend([2, 5, 0.1])


if __name__ == "__main__":
    winner = _main()
    print(winner)
