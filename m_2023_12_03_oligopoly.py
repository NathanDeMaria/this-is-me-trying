from collections import Counter
import random
from typing import Iterator
from tqdm import tqdm
import matplotlib.pyplot as plt
from fire import Fire


def _roll(n_dice: int) -> int:
    return sum(random.randint(1, 6) for _ in range(n_dice))


def _simulate_board_run(board_length: int, n_dice: int) -> Iterator[int]:
    """Simulate a run around the board, returns all positions landed on."""
    current_location = 0
    while current_location < board_length:
        yield current_location
        current_location += _roll(n_dice)


def main(
    n_trials: int = 1_000_000,
    board_length: int = 40,
    n_dice: int = 2,
    min_board_square: int = 0,
) -> None:
    """
    https://thefiddler.substack.com/p/can-you-race-around-the-monopoly

    1 million takes ~30 seconds on my laptop
    """
    counts: Counter[int] = Counter()
    for _ in tqdm(range(n_trials)):
        for position in _simulate_board_run(board_length, n_dice=n_dice):
            if position >= min_board_square:
                counts[position] += 1

    positions = list(range(board_length))
    pcts = [counts[position] / n_trials for position in positions]
    plt.bar(positions, pcts)
    plt.xlabel("Position")
    plt.ylabel("% of runs that hit this position")
    plt.ylim(0, 1)
    plt.savefig("oligopoly.png")
    frequencies = counts.most_common()
    print(f"Max: {frequencies[0]}")
    print(f"Min: {frequencies[-1]}")


if __name__ == "__main__":
    Fire(main)
