"""Optional style reference for Signal-generated plots.

Signal is not a plotting package. Copy/adapt this file into a target project's
plots directory when a shared local style is useful. Generated plots should not
import Signal itself at runtime.
"""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy

PALETTES = {
    "signal": {
        "background": "#FCFBF7",
        "foreground": "#252525",
        "grid": "#D9D7D0",
        "primary": "#315F7D",
        "secondary": "#C47A44",
        "highlight": "#B4443C",
        "context": "#AAA9A4",
        "uncertainty": "#8BA3B2",
        "positive": "#4D7C5B",
        "negative": "#A54A47",
    },
    "accessible": {
        "background": "#FFFFFF",
        "foreground": "#202020",
        "grid": "#D8D8D8",
        "primary": "#0072B2",
        "secondary": "#E69F00",
        "highlight": "#D55E00",
        "context": "#999999",
        "uncertainty": "#56B4E9",
        "positive": "#009E73",
        "negative": "#CC79A7",
    },
    "mono": {
        "background": "#FFFFFF",
        "foreground": "#202020",
        "grid": "#DDDDDD",
        "primary": "#303030",
        "secondary": "#666666",
        "highlight": "#111111",
        "context": "#AAAAAA",
        "uncertainty": "#BEBEBE",
        "positive": "#444444",
        "negative": "#777777",
    },
    "dark": {
        "background": "#171717",
        "foreground": "#F2F2F2",
        "grid": "#3A3A3A",
        "primary": "#76A9C9",
        "secondary": "#E1A06F",
        "highlight": "#EF746B",
        "context": "#777777",
        "uncertainty": "#55788D",
        "positive": "#79B88D",
        "negative": "#DD7B78",
    },
}

PROFILES = {
    "paper": {
        "figsize": (3.4, 2.5),
        "font_size": 8.5,
        "title_size": 9.5,
        "label_size": 8.5,
        "tick_size": 7.5,
        "legend_size": 7.5,
        "line_width": 1.35,
        "marker_size": 4.5,
        "dpi": 300,
    },
    "slides": {
        "figsize": (9.0, 5.0),
        "font_size": 17.0,
        "title_size": 21.0,
        "label_size": 17.0,
        "tick_size": 14.0,
        "legend_size": 14.0,
        "line_width": 2.4,
        "marker_size": 7.5,
        "dpi": 160,
    },
    "screen": {
        "figsize": (7.0, 4.2),
        "font_size": 11.0,
        "title_size": 13.0,
        "label_size": 11.0,
        "tick_size": 9.5,
        "legend_size": 9.5,
        "line_width": 1.7,
        "marker_size": 5.5,
        "dpi": 160,
    },
    "exploratory": {
        "figsize": (7.0, 4.4),
        "font_size": 10.0,
        "title_size": 12.0,
        "label_size": 10.0,
        "tick_size": 9.0,
        "legend_size": 9.0,
        "line_width": 1.5,
        "marker_size": 5.0,
        "dpi": 120,
    },
}

DEFAULT_FONT_FAMILY = "DejaVu Sans"


def palette(name: str = "signal") -> dict[str, str]:
    if name not in PALETTES:
        raise KeyError(f"Unknown palette: {name!r}. Available: {sorted(PALETTES)}")
    return dict(PALETTES[name])


def profile(name: str = "screen") -> dict[str, object]:
    if name not in PROFILES:
        raise KeyError(f"Unknown profile: {name!r}. Available: {sorted(PROFILES)}")
    return deepcopy(PROFILES[name])


@contextmanager
def style_context(
    profile_name: str = "screen",
    palette_name: str = "signal",
    *,
    font_family: list[str] | str | None = None,
):
    """Scoped Matplotlib defaults for examples and project-local reuse."""
    import matplotlib as mpl

    colors = palette(palette_name)
    cfg = profile(profile_name)
    family = DEFAULT_FONT_FAMILY if font_family is None else font_family

    rc = {
        "figure.figsize": cfg["figsize"],
        "figure.facecolor": colors["background"],
        "axes.facecolor": colors["background"],
        "savefig.facecolor": colors["background"],
        "text.color": colors["foreground"],
        "axes.labelcolor": colors["foreground"],
        "axes.edgecolor": colors["foreground"],
        "xtick.color": colors["foreground"],
        "ytick.color": colors["foreground"],
        "font.family": family,
        "font.size": cfg["font_size"],
        "axes.titlesize": cfg["title_size"],
        "axes.labelsize": cfg["label_size"],
        "xtick.labelsize": cfg["tick_size"],
        "ytick.labelsize": cfg["tick_size"],
        "legend.fontsize": cfg["legend_size"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "grid.color": colors["grid"],
        "lines.linewidth": cfg["line_width"],
        "lines.markersize": cfg["marker_size"],
        "figure.dpi": cfg["dpi"],
        "savefig.dpi": cfg["dpi"],
    }
    with mpl.rc_context(rc):
        yield colors, cfg
