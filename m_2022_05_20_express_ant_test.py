import math
import numpy as np
from m_2022_05_20_express_ant import crawl_radially


def test_vertical():
    position = crawl_radially((0, 1))
    assert position == (0, 2)


def test_horizontal():
    position = crawl_radially((1, 0))
    assert position == (2, 0)


def test_line():
    position = crawl_radially((1, 1))
    end_coordinate = 1 + math.sqrt(2) / 2
    np.testing.assert_almost_equal(position, (end_coordinate, end_coordinate))


def test_high_slope():
    position = crawl_radially((3, 4))
    np.testing.assert_almost_equal(position, (3.6, 4.8))


def test_low_slope():
    position = crawl_radially((4, 3))
    np.testing.assert_almost_equal(position, (4.8, 3.6))
