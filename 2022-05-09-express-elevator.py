"""
From Starvind comes a matter of a frustrating (but not terrifying) tower:

You are on the 10th floor of a tower and want to exit on the first floor.
You get into the elevator and hit 1.
However, this elevator is malfunctioning in a specific way.
When you hit 1, it correctly registers the request to descend,
but it randomly selects some floor below your current floor (including the first floor).
The car then stops at that floor.
If it's not the first floor, you again hit 1 and the process repeats.

Assuming you are the only passenger on the elevator,
how many floors on average will it stop at
(including your final stop, the first floor) until you exit?

https://fivethirtyeight.com/features/can-you-build-the-longest-ladder/
"""
import math
from fractions import Fraction


def get_expected_floors(n: int) -> Fraction:
    if n < 1:
        raise ValueError("Floors start at 1")
    if n == 1:
        return Fraction(0, 1)
    return 1 + Fraction(sum(map(get_expected_floors, range(2, n))) , (n - 1))


def _sterling(n: int, k: int) -> int:
    if n == 0 and k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    return (n - 1) * _sterling(n - 1, k) + _sterling(n - 1, k - 1)


def pretty():
    """
    Be verbose so that I notice the pattern

    | S(n, 2) | / (n - 1)!
    """
    fractions = [get_expected_floors(n) for n in range(2, 12)]

    # This is how I got to see the pattern
    # for i, fraction in enumerate(fractions):
    #     n = i + 2
    #     f = math.factorial(n)
    #     scalar = f / fraction.denominator
    #     print(fraction.numerator * scalar / n, f, _sterling(n, 2), float(fraction))

    for n, fraction in enumerate(fractions, start=2):
        print(float(fraction), _sterling(n, 2) / math.factorial(n - 1))


if __name__ == '__main__':
    pretty()
