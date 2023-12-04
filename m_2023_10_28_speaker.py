from math import comb
import numpy as np
from tqdm import tqdm

_N_VOTERS = 221


# Is it just 3x the probability that 1/3 rolls more than _N_VOTERS / 2?
# 3 * (1 - binomial CDF of at 110)
def _the_math_way(n_candidates: int) -> float:
    assert _N_VOTERS % 2 == 1, "This won't work if there's an even #"
    votes_with_a_loss = _N_VOTERS // 2
    # https://en.wikipedia.org/wiki/Binomial_distribution#:~:text=0.059535.-,Cumulative%20distribution%20function,-%5Bedit%5D
    p = 1 / n_candidates
    chance_one_candidate_wins = 1 - sum(
        comb(_N_VOTERS, i) * (p**i) * ((1 - p) ** (_N_VOTERS - i))
        for i in range(votes_with_a_loss + 1)
    )
    return chance_one_candidate_wins * n_candidates


def _the_mc_way(n_candidates: int, n_samples: int = 1_000_000) -> float:
    # 1m iterations took ~1 minute on my laptop
    found: list[bool] = []
    for _ in tqdm(range(n_samples)):
        votes = np.random.randint(low=0, high=n_candidates, size=_N_VOTERS)
        _, counts = np.unique(votes, return_counts=True)
        found.append(counts.max() > _N_VOTERS // 2)
    return np.mean(found)


def main(n_candidates: int = 3):
    """
    https://thefiddler.substack.com/p/how-long-would-it-take-to-pick-a
    """
    print(_the_math_way(n_candidates=n_candidates))
    print(_the_mc_way(n_candidates=n_candidates))


if __name__ == "__main__":
    main()
