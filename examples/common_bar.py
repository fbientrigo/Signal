from pathlib import Path
import sys

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "themes"))
from signal_style import style_context  # noqa: E402

labels = ["baseline", "method A", "method B", "candidate"]
values = [61, 68, 72, 79]

with style_context("slides") as (colors, _profile):
    fig, ax = plt.subplots(layout="constrained")
    bar_colors = [colors["context"]] * 3 + [colors["highlight"]]
    ax.bar(labels, values, color=bar_colors)
    ax.set(ylabel="Score", ylim=(0, 85), title="Common things should stay simple")
    out = Path(__file__).with_suffix(".png")
    fig.savefig(out)
    print(out)
