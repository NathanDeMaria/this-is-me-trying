"""
https://fivethirtyeight.com/features/can-you-escape-the-desert/
"""
import logging
from itertools import permutations, product
from typing import Callable, Iterable, Sequence, Iterator
from math import prod

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger()


_Operation = Callable[[Iterable[int]], int]
_OPERATIONS: list[_Operation] = [sum, prod]


def _create_slices(num_components: int) -> list[list[slice]]:
    slice_groups = []
    slice_locations = product(*(range(2) for _ in range(num_components - 1)))
    for slice_on in slice_locations:
        start = 0
        slices = []
        for i, has_break in enumerate(slice_on):
            if not has_break:
                slices.append(slice(start, i + 1))
                start = i + 1
        if start != num_components:
            slices.append(slice(start, num_components))
        slice_groups.append(slices)
    return slice_groups


def _combine(items: Sequence[int], operations: Sequence[_Operation]) -> int:
    assert len(items) - 1 == len(operations)
    final = items[0]
    for operation, i in zip(operations, items[1:]):
        final = operation([final, i])
    return final


def _get_value(
    items: Sequence[int], groupings: Sequence[slice], operations: Sequence[_Operation]
) -> int:
    group_results = []
    for group in groupings:
        group_items = items[group]
        group_len = len(group_items)
        if group_len == 1:
            group_results.append(group_items[0])
        else:
            group_results.append(_combine(group_items, operations[: group_len - 1]))
            operations = operations[group_len - 1 :]
    return _combine(group_results, operations)


def _grid(length: int) -> Iterator[tuple[_Operation, ...]]:
    return product(*(_OPERATIONS for _ in range(length)))


def _all_results(items: list[int]) -> set[int]:
    item_lists = [p for n in range(len(items)) for p in permutations(items, 1 + n)]
    all_results = set()
    # Could definitely be more clever than
    # all combos of orderings, operators, and parentheses
    # But I trust this more than my ability to prune effectively
    for item_list in item_lists:
        operation_sets = _grid(len(item_list) - 1)
        for operation_set in operation_sets:
            all_groupings = _create_slices(len(item_list))
            for groupings in all_groupings:
                result = _get_value(item_list, groupings, operation_set)
                all_results.add(result)
    return all_results


def _first_missing(all_results: set[int]) -> int:
    sorted_results = sorted(all_results)
    return next(
        (i for i, result in enumerate(sorted_results, start=1) if i != result),
        default=sorted_results[-1] + 1,
    )


if __name__ == "__main__":
    """
    This took ~5 hours to get FUN(8)
    """
    for n in range(1, 50):
        results = _all_results(list(range(1, n + 1)))
        message = f"{n}\t{_first_missing(results)}"
        logger.info(message)
