"""
https://fivethirtyeight.com/features/can-you-spot-the-black-hole/
"""
import random
import math
import numpy as np
from tqdm import tqdm


_Position = tuple[float, float]


def crawl(position: _Position, radial: bool) -> _Position:
    """
    Crawl the ant 1 meter

    If radial is true, crawl outward directly from the center.
    If false, crawl on a tangent
    """
    x, y = position
    if x == 0:
        return (0, y + 1) if radial else (1, y)
    if y == 0:
        return (x + 1, 0) if radial else (x, 1)
    slope = y / x if radial else -x / y
    x_distance = math.sqrt(1 / (1 + slope**2))
    y_distance = x_distance * slope
    return x + x_distance, y + y_distance


def _crawl(n: int = 4) -> float:
    # WLOG, say we moved up first
    position = (0.0, 1.0)
    for _ in range(n - 1):
        position = crawl(position, random.random() < 0.5)
    return np.linalg.norm(position).item()


def _manually() -> list[float]:
    return [
        # rrrr
        4,
        # rrrt
        math.sqrt(10),
        # rrtr
        math.sqrt(5) + 1,
        # rrtt
        math.sqrt(6),
        # rtrr
        2 + math.sqrt(2),
        # rtrt
        math.sqrt(4 + 2 * math.sqrt(2)),
        # rttr
        math.sqrt(3) + 1,
        # rttt
        2,
    ]


def main():
    end_positions = [_crawl() for _ in tqdm(range(int(1e6)))]
    print(np.mean(end_positions))
    # Checking that I got everything correct manually
    manual = _manually()
    print(f"{np.mean(manual)=}")
    unique_ends = sorted(set(end_positions))
    np.testing.assert_allclose(unique_ends, sorted(manual))


if __name__ == "__main__":
    main()
