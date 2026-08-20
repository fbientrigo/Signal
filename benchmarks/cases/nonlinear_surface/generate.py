"""Generates data.csv for the nonlinear_surface benchmark case.

Evaluator-side only. Never copy this file into an agent workspace —
the generating function must stay unknown to the evaluated agent.
Deterministic (fixed seed): rerunning reproduces byte-identical output.

Structure, by construction:
  - optimum humidity shifts with temperature (curved ridge, not a fixed
    peak) -> genuine interaction between the two inputs;
  - Gaussian falloff away from the ridge -> degradation with no simple
    monotonic relationship to either input alone;
  - a smaller secondary local bump elsewhere -> a second local feature;
  - output clipped to [0, 100] -> bounded quantity;
  - small deterministic noise so the surface isn't perfectly smooth.

Adversarial packaging (row-order, not signal structure):
  - rows are shuffled (defeats "plot row order as a line/series");
  - a handful of cells are dropped (defeats "assume a complete rectangular
    grid without checking").
"""
import csv
import math
from pathlib import Path

import numpy as np

OUT = Path(__file__).parent / "data.csv"
SEED = 20260818

T_VALUES = list(range(15, 36, 1))       # temperature_c: 15..35, 21 values
H_VALUES = list(range(20, 81, 4))       # humidity_pct: 20..80, 16 values

T_OPT = 24.0
SECOND_T, SECOND_H = 32.0, 28.0


def humidity_ridge(t: float) -> float:
    # optimum humidity is not fixed: it curves with temperature
    return 55.0 + 6.0 * math.sin((t - 15.0) / 20.0 * math.pi)


def performance(t: float, h: float, rng: np.random.Generator) -> float:
    h_opt = humidity_ridge(t)
    main = 100.0 * math.exp(-(((t - T_OPT) / 6.0) ** 2 + ((h - h_opt) / 16.0) ** 2))
    second = 20.0 * math.exp(-(((t - SECOND_T) / 2.5) ** 2 + ((h - SECOND_H) / 4.0) ** 2))
    noise = float(rng.normal(0.0, 1.5))
    return max(0.0, min(100.0, main + second + noise))


def main() -> None:
    rng = np.random.default_rng(SEED)

    rows = []
    for t in T_VALUES:
        for h in H_VALUES:
            rows.append((t, h, round(performance(t, h, rng), 2)))

    # drop a small, deterministic set of cells (missing data, not at random pattern)
    drop_rng = np.random.default_rng(SEED + 1)
    drop_idx = set(drop_rng.choice(len(rows), size=5, replace=False).tolist())
    rows = [r for i, r in enumerate(rows) if i not in drop_idx]

    # shuffle row order deterministically
    shuffle_rng = np.random.default_rng(SEED + 2)
    order = shuffle_rng.permutation(len(rows))
    rows = [rows[i] for i in order]

    with OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["temperature_c", "humidity_pct", "performance"])
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
