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
    point_colors = [colors["context"]] * 3 + [colors["highlight"]]
    y = range(len(labels))
    ax.scatter(values, y, s=48, color=point_colors, zorder=3)
    ax.set_yticks(list(y), labels)
    ax.set(
        xlabel="Score",
        xlim=(55, 82),
        title="Compare categories on a common scale",
    )
    out = Path(__file__).with_suffix(".png")
    fig.savefig(out)
    print(out)
