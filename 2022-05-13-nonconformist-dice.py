"""
https://fivethirtyeight.com/features/its-elementary-my-dear-riddler/
"""
import random
from collections import Counter
from enum import Enum, auto
from fractions import Fraction
import numpy as np
from tqdm import tqdm


class State(Enum):
    """
    The four dice have to be in one of these states.
    """

    SAME = auto()
    UNIQUE = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE = auto()


_N_DICE = 4
_VALUES = [1, 2, 3, 4]
_INITIAL_ROLL = {
    # 4 ways
    State.SAME: Fraction(1, 4 * 4 * 4),
    # 4! ways
    State.UNIQUE: Fraction(3, 4 * 4 * 2),
    # 4 (for the pair) * 3 (for one unique) * 2 (2nd unique) * 3! ways to slot the pairs
    State.ONE_PAIR: Fraction(3 * 3, 4 * 4),
    # 4 for the first pair, 3 for the 2nd, 3 ways to arrange it
    State.TWO_PAIR: Fraction(3 * 3, 4 * 4 * 4),
    # 4 for the triple, 3 for extra, 4 places to put the extra
    State.THREE: Fraction(3, 4 * 4),
}
_TRANSITIONS: dict[State, dict[State, Fraction]] = {
    # These are done
    State.SAME: {State.SAME: Fraction(1, 1)},
    State.UNIQUE: {
        State.UNIQUE: Fraction(1, 1),
    },
    State.TWO_PAIR: {State.TWO_PAIR: Fraction(1, 1)},
    # These reroll
    State.ONE_PAIR: {
        State.SAME: Fraction(0, 1),
        # 2 ways (different from the 2 existing, flip)
        State.UNIQUE: Fraction(1, 4 * 2),
        # 2 ways (match the 2 existing, flip)
        State.TWO_PAIR: Fraction(1, 4 * 2),
        # Pair made with one of two non-rolled dice
        # 2 for the first (to match), 2 (to not match),
        # and *2 to flip (matching die comes second)
        # OR pair made on the rolled dice (2 ways)
        State.ONE_PAIR: Fraction(2 * 2 + 1, 4 * 2),
        # 2 ways (roll the same, and match one of the existing)
        State.THREE: Fraction(1, 4 * 2),
    },
    State.THREE: {
        # All 3 rolled have to match the other, so 1 way
        State.SAME: Fraction(1, 4 * 4 * 4),
        # 3 (for the first) * 2 (for the second) * 1 (3rd is forced)
        State.UNIQUE: Fraction(3, 4 * 4 * 2),
        # 3 values for the "new" pair, 3 slots for the die that pairs with the unrolled
        State.TWO_PAIR: Fraction(3 * 3, 4 * 4 * 4),
        # Pair is with the unrolled
        # 3 positions for the matching die * 3 for the first non-match, 2 for the 2nd
        # OR pair is in the new die
        # 3 values for the pair * 3 positions for the other unique * 2 values for it
        State.ONE_PAIR: Fraction(3 * 3, 4 * 4),
        # 3 triple includes the new die (3 values for the other * 3 spots for it)
        # OR triple doesn't include the new one (3 ways - the 3 other values)
        State.THREE: Fraction(3, 4 * 4),
    },
}
assert sum(_INITIAL_ROLL.values()) == 1
for transitions in _TRANSITIONS.values():
    assert sum(transitions.values()) == 1

_END_STATES = frozenset([State.UNIQUE, State.TWO_PAIR, State.SAME])


def _roll(fixed: list[int] = None) -> list[int]:
    if fixed is None:
        fixed = []
    n_rolled = _N_DICE - len(fixed)
    return fixed + random.choices(_VALUES, k=n_rolled)


def _get_state(dice: list[int]) -> State:
    counts = sorted(Counter(dice).values())
    if counts == [1, 1, 2]:
        return State.ONE_PAIR
    if counts == [1, 3]:
        return State.THREE
    if counts == [2, 2]:
        return State.TWO_PAIR
    if counts == [1, 1, 1, 1]:
        return State.UNIQUE
    return State.SAME


def _get_unique(dice: list[int]) -> list[int]:
    return [d for d, c in Counter(dice).items() if c == 1]


def do_the_math(iterations: int):
    """
    Find the answer by getting the transition matrix, and then finding the steady state.
    """
    transition_matrix = np.zeros((len(State), len(State)), dtype=float)
    for i, from_state in enumerate(State):
        for j, to_state in enumerate(State):
            transition_matrix[i, j] = float(_TRANSITIONS[from_state].get(to_state, 0))
    current_state = np.array([_INITIAL_ROLL[state] for state in State])
    for _ in range(iterations):
        current_state = np.matmul(current_state, transition_matrix)
    return current_state[list(State).index(State.UNIQUE)]


def _simulate() -> bool:
    dice = _roll()
    state = _get_state(dice)
    while state not in _END_STATES:
        fixed_dice = _get_unique(dice)
        dice = _roll(fixed_dice)
        state = _get_state(dice)
    return state is State.UNIQUE


def simulate(samples: int):
    """
    Monte Carlo to check my math.
    """
    return np.mean([_simulate() for _ in tqdm(range(samples))])


if __name__ == "__main__":
    print(f"{do_the_math(1000)=}")
    print(f"{simulate(int(1e6))=}")
