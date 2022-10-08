"""
https://fivethirtyeight.com/features/can-you-fold-all-your-socks/
"""
import logging
from datetime import datetime
from itertools import product


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
_logger = logging.getLogger()


_SEARCH_SPACE = [
    # Year
    list(range(2, 10)),  # Can't start with a 1 or 0
    list(range(10)),
    list(range(10)),
    list(range(10)),
    # Hour
    [0, 1],
    list(range(10)),
    # Minute
    list(range(6)),
    [8],
    # Second
    list(range(6)),
    [9],  # I can thin the search space by knowing this is the best place to put a 9
]


def main():
    now = datetime.utcnow()
    for slot in product(*_SEARCH_SPACE):
        if len(set(slot)) != 10:
            continue
        (
            millenium,
            century,
            decade,
            year,
            ten_hour,
            hour,
            ten_minutes,
            minutes,
            ten_seconds,
            seconds,
        ) = slot
        if ten_hour == hour == 0:
            # 00 isn't a valid hour
            continue
        if ten_hour == 1 and hour > 2:
            # Neither is anything >= 13
            continue
        test_time = datetime(
            year=millenium * 1000 + century * 100 + decade * 10 + year,
            # I know it's not this year, so the soonest valid one will be Jan 1st.
            month=1,
            day=1,
            hour=ten_hour * 10 + hour,
            minute=10 * ten_minutes + minutes,
            second=10 * ten_seconds + seconds,
        )
        if test_time > now:
            _logger.info(test_time)
            return


if __name__ == "__main__":
    main()
