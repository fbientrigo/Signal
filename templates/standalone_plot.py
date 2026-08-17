"""Template for a durable, manually editable plot script."""
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".png")


def main() -> None:
    # Load/prepare data here. Keep transformations explicit.
    x = [1, 2, 3, 4]
    y = [2.0, 2.8, 3.1, 4.2]

    fig, ax = plt.subplots(figsize=(6.0, 3.8), layout="constrained")
    ax.plot(x, y, marker="o")
    ax.set(xlabel="x", ylabel="y")
    fig.savefig(OUT, dpi=180)
    print(OUT)


if __name__ == "__main__":
    main()
