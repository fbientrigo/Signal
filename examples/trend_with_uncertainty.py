from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "themes"))
from signal_style import style_context  # noqa: E402

mass = np.array([80, 100, 125, 150, 200, 250, 300])
estimate = np.array([0.08, 0.15, 0.27, 0.39, 0.51, 0.57, 0.60])
low = np.array([0.05, 0.11, 0.22, 0.33, 0.45, 0.50, 0.53])
high = np.array([0.12, 0.20, 0.33, 0.46, 0.58, 0.64, 0.67])
benchmark = 150

yerr = np.vstack([estimate - low, high - estimate])

with style_context("paper") as (colors, _profile):
    fig, ax = plt.subplots(layout="constrained")
    ax.errorbar(
        mass,
        estimate,
        yerr=yerr,
        fmt="o-",
        capsize=2.5,
        color=colors["primary"],
        ecolor=colors["uncertainty"],
        label="Selection efficiency",
    )
    ax.axvline(benchmark, color=colors["context"], linestyle="--", linewidth=1.0)
    idx = int(np.flatnonzero(mass == benchmark)[0])
    ax.scatter([mass[idx]], [estimate[idx]], s=34, color=colors["highlight"], zorder=4)
    ax.annotate(
        "benchmark",
        xy=(mass[idx], estimate[idx]),
        xytext=(6, 8),
        textcoords="offset points",
        color=colors["highlight"],
    )
    ax.set(
        xlabel=r"Mass [GeV]",
        ylabel="Efficiency",
        ylim=(0, 0.75),
        title="Trend with asymmetric uncertainty",
    )
    ax.legend(frameon=False, loc="lower right")
    out = Path(__file__).with_suffix(".png")
    fig.savefig(out)
    print(out)
