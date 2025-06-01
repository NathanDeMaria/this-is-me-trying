import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def _create_line_grid(size: int = 1_000, iterations: int = 10_000_000) -> np.ndarray:
    # This took ~30 minutes on my laptop
    grid = np.zeros((size, size), dtype=int)
    for _ in tqdm(range(iterations)):
        _append_points(grid)
    return grid / iterations


def _append_points(grid: np.ndarray) -> None:
    x1, y1 = np.random.randint(0, grid.shape[0], 2)
    x2, y2 = np.random.randint(0, grid.shape[1], 2)

    # Handle vertical line case
    if x1 == x2:
        grid[:, x1] += 1
        return

    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    x = np.arange(0, grid.shape[0])
    y = np.round(m * x + b).astype(int)

    # Ensure y values are within grid bounds
    mask = (y >= 0) & (y < grid.shape[1])
    np.add.at(grid, (y[mask], x[mask]), 1)


def _main() -> None:
    grid = _create_line_grid()
    plt.imshow(grid, cmap="viridis", origin="lower")
    plt.colorbar()
    plt.savefig(f"{__file__.split('.')[0]}.png")


if __name__ == "__main__":
    _main()
