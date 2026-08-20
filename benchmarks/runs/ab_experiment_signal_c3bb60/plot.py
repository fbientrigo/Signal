"""A/B Test Conversion Rate Visualization.

Produces a scientifically rigorous visualization comparing conversion rates
and effect sizes between Variant A and Variant B with 95% confidence intervals.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from scipy import stats


def wilson_ci(k: int, n: int, confidence: float = 0.95) -> tuple[float, float, float]:
    """Calculate conversion rate and Wilson score confidence interval."""
    p = k / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    z2 = z ** 2
    denominator = 1 + z2 / n
    center = (p + z2 / (2 * n)) / denominator
    half_width = (z / denominator) * np.sqrt((p * (1 - p) / n) + (z2 / (4 * n ** 2)))
    return p, max(0.0, center - half_width), min(1.0, center + half_width)


def main():
    # Load dataset
    data_path = Path(__file__).parent / "data.csv"
    if not data_path.exists():
        data_path = Path("data.csv")
    df = pd.read_csv(data_path)

    # Extract counts
    row_a = df[df["variant"] == "A"].iloc[0]
    row_b = df[df["variant"] == "B"].iloc[0]

    n_a, k_a = int(row_a["visitors"]), int(row_a["conversions"])
    n_b, k_b = int(row_b["visitors"]), int(row_b["conversions"])

    # Compute rates and Wilson 95% CIs
    p_a, low_a, high_a = wilson_ci(k_a, n_a)
    p_b, low_b, high_b = wilson_ci(k_b, n_b)

    # Compute effect size and two-proportion z-test
    diff = p_b - p_a
    rel_diff = (p_b - p_a) / p_a

    # Standard error of difference (unpooled for CI)
    se_diff_unpooled = np.sqrt((p_a * (1 - p_a) / n_a) + (p_b * (1 - p_b) / n_b))
    z_crit = stats.norm.ppf(0.975)
    diff_ci_low = diff - z_crit * se_diff_unpooled
    diff_ci_high = diff + z_crit * se_diff_unpooled

    # Pooled standard error for hypothesis testing
    p_pool = (k_a + k_b) / (n_a + n_b)
    se_diff_pooled = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z_stat = (p_b - p_a) / se_diff_pooled
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # Signal aesthetic palette
    bg_color = "#FCFBF7"
    fg_color = "#252525"
    grid_color = "#E5E3DC"
    color_a = "#315F7D"      # Slate blue
    color_b = "#C47A44"      # Warm terracotta
    color_diff = "#B4443C"   # Muted red for negative difference

    # Style configuration
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "text.color": fg_color,
        "axes.labelcolor": fg_color,
        "axes.edgecolor": fg_color,
        "xtick.color": fg_color,
        "ytick.color": fg_color,
        "figure.facecolor": bg_color,
        "axes.facecolor": bg_color,
        "savefig.facecolor": bg_color,
    })

    # Create figure with 2 subplots (Estimation plot style)
    fig, (ax1, ax2) = plt.subplots(
        1, 2,
        figsize=(8.6, 4.6),
        gridspec_kw={"width_ratios": [1.35, 1.0]},
        dpi=300
    )

    # -------------------------------------------------------------
    # Panel 1: Conversion Rates with 95% Wilson Confidence Intervals
    # -------------------------------------------------------------
    x_pos = np.array([0, 1])
    rates = np.array([p_a, p_b]) * 100
    yerr_lower = np.array([p_a - low_a, p_b - low_b]) * 100
    yerr_upper = np.array([high_a - p_a, high_b - p_b]) * 100
    yerr = np.vstack([yerr_lower, yerr_upper])

    ax1.bar(
        x_pos,
        rates,
        width=0.45,
        color=[color_a, color_b],
        alpha=0.88,
        edgecolor=[color_a, color_b],
        linewidth=1.2,
        zorder=3
    )

    ax1.errorbar(
        x_pos,
        rates,
        yerr=yerr,
        fmt="none",
        ecolor=fg_color,
        elinewidth=1.4,
        capsize=4.5,
        capthick=1.4,
        zorder=4
    )

    # Add data annotations above error bars
    for i, (p_val, low_val, high_val) in enumerate([
        (p_a, low_a, high_a),
        (p_b, low_b, high_b)
    ]):
        y_top = high_val * 100
        ax1.text(
            i,
            y_top + 0.15,
            f"{p_val * 100:.2f}%\n[95% CI: {low_val * 100:.2f}–{high_val * 100:.2f}%]",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color=fg_color
        )

    x_labels = [
        f"Variant A (Baseline)\nn = {n_a:,} ({k_a:,} conv.)",
        f"Variant B\nn = {n_b:,} ({k_b:,} conv.)"
    ]
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(x_labels, fontsize=9.0, fontweight="bold")
    ax1.set_ylabel("Conversion Rate (%)", fontsize=10, fontweight="bold")
    ax1.set_ylim(0, 5.4)
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(100, decimals=1))
    ax1.grid(axis="y", color=grid_color, linestyle="-", linewidth=0.75, zorder=0)
    ax1.set_title("Conversion Rate by Variant", fontsize=11, fontweight="bold", pad=12)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_linewidth(0.8)
    ax1.spines["bottom"].set_linewidth(0.8)

    # -------------------------------------------------------------
    # Panel 2: Effect Size & Difference (Variant B vs Variant A)
    # -------------------------------------------------------------
    diff_pct = diff * 100
    diff_ci_low_pct = diff_ci_low * 100
    diff_ci_high_pct = diff_ci_high * 100

    # Reference line at 0 (No difference)
    ax2.axhline(0, color="#777777", linestyle="--", linewidth=1.1, zorder=2)
    ax2.text(
        0.55, 0.05, "No difference",
        transform=ax2.get_yaxis_transform(),
        color="#666666", fontsize=8.0, va="bottom", ha="right"
    )

    # Plot difference point with error bar
    diff_yerr = np.array([[diff_pct - diff_ci_low_pct], [diff_ci_high_pct - diff_pct]])
    ax2.errorbar(
        [0],
        [diff_pct],
        yerr=diff_yerr,
        fmt="o",
        color=color_diff,
        ecolor=color_diff,
        elinewidth=1.6,
        capsize=5.0,
        capthick=1.5,
        markersize=7.0,
        zorder=4
    )

    # Annotate effect size details
    stat_text = (
        f"Δ = {diff_pct:+.2f} pp\n"
        f"95% CI: [{diff_ci_low_pct:.2f}, {diff_ci_high_pct:.2f}] pp\n"
        f"Relative: {rel_diff * 100:+.1f}%\n"
        f"p = {p_value:.4f} (z = {z_stat:.2f})"
    )
    ax2.text(
        0.12,
        diff_pct,
        stat_text,
        ha="left",
        va="center",
        fontsize=8.5,
        color=fg_color,
        bbox=dict(boxstyle="round,pad=0.45", facecolor=bg_color, edgecolor=grid_color, linewidth=0.8)
    )

    ax2.set_xticks([0])
    ax2.set_xticklabels(["Variant B − Variant A\n(Difference)"], fontsize=9.0, fontweight="bold")
    ax2.set_ylabel("Difference (Percentage Points)", fontsize=10, fontweight="bold")
    ax2.set_xlim(-0.35, 0.75)
    ax2.set_ylim(-2.2, 0.8)

    # Format y-axis cleanly without + on 0.0
    def pp_formatter(val, pos):
        if np.isclose(val, 0):
            return "0.0 pp"
        return f"{val:+.1f} pp"

    ax2.yaxis.set_major_formatter(mtick.FuncAnimation if False else mtick.FuncFormatter(pp_formatter))
    ax2.grid(axis="y", color=grid_color, linestyle="-", linewidth=0.75, zorder=0)
    ax2.set_title("Effect Size (B vs A)", fontsize=11, fontweight="bold", pad=12)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_linewidth(0.8)
    ax2.spines["bottom"].set_linewidth(0.8)

    # -------------------------------------------------------------
    # Overall Title and Footnote
    # -------------------------------------------------------------
    fig.suptitle(
        "A/B Experiment: Conversion Rate Comparison",
        fontsize=13,
        fontweight="bold",
        x=0.08,
        ha="left",
        y=0.98
    )

    fig.text(
        0.08,
        0.02,
        "Note: Left error bars denote 95% Wilson score confidence intervals; right error bar denotes 95% Wald CI for difference. p-value from two-sided two-proportion z-test.",
        fontsize=7.5,
        color="#666666",
        ha="left"
    )

    plt.subplots_adjust(left=0.09, right=0.95, top=0.86, bottom=0.17, wspace=0.35)

    # Save output
    output_path = Path(__file__).parent / "plot.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Plot successfully saved to {output_path}")


if __name__ == "__main__":
    main()
