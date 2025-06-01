import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def _create_line_grid(size: int = 1_000, iterations: int = 10_000) -> np.ndarray:
    # Create a grid of zeros
    grid = np.zeros((size, size), dtype=int)
    for _ in tqdm(range(iterations)):
        _append_points(grid)
    return grid / iterations



def _append_points(grid: np.ndarray) -> None:
    # Generate two random points (x1, y1) and (x2, y2)
    x1, y1 = np.random.randint(0, grid.shape[0], 2)
    x2, y2 = np.random.randint(0, grid.shape[1], 2)

    # Handle vertical line case
    if x1 == x2:
        grid[:, x1] += 1
        return

    # Calculate slope and intercept for the line equation y = mx + b
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    # For each x coordinate, find the nearest y on the line
    for x in range(0, grid.shape[0]):
        y = m * x + b
        # Round to nearest integer and clamp to grid bounds
        y_round = int(round(y))
        if 0 <= y_round < grid.shape[1]:
            grid[y_round, x] += 1


def _main() -> None:
    grid = _create_line_grid()
    plt.imshow(grid, cmap="viridis", origin="lower")
    plt.colorbar()
    plt.savefig(f"{__file__.split('.')[0]}.png")


if __name__ == "__main__":
    _main()
