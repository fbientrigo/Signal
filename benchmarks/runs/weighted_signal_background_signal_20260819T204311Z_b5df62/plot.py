"""Plot comparison of signal and background score distributions.

Preserves weighted yield (unnormalized) and calculates bin-by-bin statistical
uncertainty from independent fixed per-event weights as sigma = sqrt(sum(w_i^2)).
Highlights the tail region above score = 0.8.
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd


def main():
    # Load dataset
    data_path = Path(__file__).parent / "data.csv" if "__file__" in globals() else Path("data.csv")
    if not data_path.exists():
        data_path = Path("data.csv")
    df = pd.read_csv(data_path)

    # Binning definition across score range [0.0, 1.0]
    bins = np.linspace(0.0, 1.0, 11)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    sig_df = df[df["sample"] == "signal"]
    bkg_df = df[df["sample"] == "background"]

    # Compute weighted yields and statistical uncertainties: sigma = sqrt(sum(w^2))
    sig_y, _ = np.histogram(sig_df["score"], bins=bins, weights=sig_df["weight"])
    sig_w2, _ = np.histogram(sig_df["score"], bins=bins, weights=sig_df["weight"] ** 2)
    sig_err = np.sqrt(sig_w2)
    sig_counts, _ = np.histogram(sig_df["score"], bins=bins)

    bkg_y, _ = np.histogram(bkg_df["score"], bins=bins, weights=bkg_df["weight"])
    bkg_w2, _ = np.histogram(bkg_df["score"], bins=bins, weights=bkg_df["weight"] ** 2)
    bkg_err = np.sqrt(bkg_w2)
    bkg_counts, _ = np.histogram(bkg_df["score"], bins=bins)

    # Totals across entire distribution
    sig_tot_y = sig_df["weight"].sum()
    sig_tot_err = np.sqrt((sig_df["weight"] ** 2).sum())
    bkg_tot_y = bkg_df["weight"].sum()
    bkg_tot_err = np.sqrt((bkg_df["weight"] ** 2).sum())

    # Tail statistics (score > 0.8)
    sig_tail_w = sig_df.loc[sig_df["score"] > 0.8, "weight"]
    sig_tail_y = sig_tail_w.sum()
    sig_tail_err = np.sqrt((sig_tail_w ** 2).sum())

    bkg_tail_w = bkg_df.loc[bkg_df["score"] > 0.8, "weight"]
    bkg_tail_y = bkg_tail_w.sum()
    bkg_tail_err = np.sqrt((bkg_tail_w ** 2).sum())

    # Visual design and colors (accessible, publication-grade)
    c_sig = "#0072B2"      # Primary blue for signal
    c_bkg = "#D55E00"      # Vermilion / amber for background
    c_tail_bg = "#F2F4F8"  # Subtle tint for tail region
    c_text = "#202020"
    c_grid = "#EAEAEA"

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8.5,
        "axes.labelsize": 9.0,
        "axes.titlesize": 10.0,
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 8.0,
        "legend.fontsize": 7.5,
        "figure.dpi": 300,
        "savefig.dpi": 300,
    })

    fig, ax = plt.subplots(figsize=(5.4, 3.8))

    # Highlight tail region (score > 0.8)
    ax.axvspan(0.8, 1.0, color=c_tail_bg, zorder=0)
    ax.axvline(0.8, color="#777777", linestyle="--", linewidth=1.0, zorder=1)

    # Grid
    ax.yaxis.grid(True, linestyle=":", alpha=0.7, color=c_grid, zorder=0)
    ax.set_axisbelow(True)

    # Step histograms showing expected yield per bin
    ax.step(bins, np.append(sig_y, sig_y[-1]), where="post", color=c_sig, lw=1.8, zorder=3)
    ax.step(bins, np.append(bkg_y, bkg_y[-1]), where="post", color=c_bkg, lw=1.8, linestyle="--", zorder=3)

    # Offset error bars for bins with events
    dx = 0.009
    sig_mask = sig_counts > 0
    bkg_mask = bkg_counts > 0

    ax.errorbar(
        bin_centers[sig_mask] + dx,
        sig_y[sig_mask],
        yerr=sig_err[sig_mask],
        fmt="o",
        color=c_sig,
        markersize=4.0,
        capsize=2.5,
        capthick=1.0,
        elinewidth=1.3,
        zorder=4,
    )

    ax.errorbar(
        bin_centers[bkg_mask] - dx,
        bkg_y[bkg_mask],
        yerr=bkg_err[bkg_mask],
        fmt="s",
        color=c_bkg,
        markersize=4.0,
        capsize=2.5,
        capthick=1.0,
        elinewidth=1.3,
        zorder=4,
    )

    # Tail callout box
    callout_text = (
        "Tail region (score > 0.8)\n"
        f"Signal yield:       {sig_tail_y:.2f} \u00b1 {sig_tail_err:.2f}\n"
        f"Background:      {bkg_tail_y:.2f} \u00b1 {bkg_tail_err:.2f}\n"
        f"Signal / Bkg:      {sig_tail_y / bkg_tail_y:.1f}\u00d7"
    )
    ax.text(
        0.815,
        4.85,
        callout_text,
        fontsize=7.2,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.95, edgecolor="#cccccc", lw=0.7),
        zorder=5,
    )

    # Axes configuration
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 5.2)
    ax.set_xlabel("Score", fontsize=9.5, color=c_text)
    ax.set_ylabel("Expected yield / 0.1 bin", fontsize=9.5, color=c_text)

    # Spines styling
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#444444")
    ax.spines["bottom"].set_color("#444444")
    ax.tick_params(colors="#444444")

    # Title and subtitle
    ax.set_title("Signal and Background Score Distributions", fontsize=10.0, loc="left", pad=14, fontweight="bold")
    ax.text(
        0.0,
        1.02,
        "Target exposure (fixed per-event weights) \u2022 Error bars: \u00b11\u03c3 stat. uncert. \u221a(\u03a3w\u00b2)",
        transform=ax.transAxes,
        fontsize=7.2,
        color="#555555",
    )

    # Legend with unified handles
    legend_handles = [
        Line2D(
            [0],
            [0],
            color=c_sig,
            lw=1.8,
            marker="o",
            markersize=4,
            label=f"Signal ($N = {len(sig_df)}$, total yield = {sig_tot_y:.2f} \u00b1 {sig_tot_err:.2f})",
        ),
        Line2D(
            [0],
            [0],
            color=c_bkg,
            lw=1.8,
            linestyle="--",
            marker="s",
            markersize=4,
            label=f"Background ($N = {len(bkg_df)}$, total yield = {bkg_tot_y:.2f} \u00b1 {bkg_tot_err:.2f})",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper left",
        frameon=True,
        facecolor="white",
        framealpha=0.95,
        edgecolor="#cccccc",
        fancybox=False,
        fontsize=7.3,
    )

    plt.tight_layout()
    output_path = Path(__file__).parent / "plot.png" if "__file__" in globals() else Path("plot.png")
    plt.savefig(output_path)
    plt.close()
    print("plot.png created successfully")


if __name__ == "__main__":
    main()
