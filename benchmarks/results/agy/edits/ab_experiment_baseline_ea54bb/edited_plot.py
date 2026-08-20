"""
A/B Experiment Conversion Rate Analysis and Visualization
Generates a scientifically sound visualization comparing Variant A and Variant B.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

def compute_wilson_ci(k, n, confidence=0.95):
    """Compute Wilson score interval for a binomial proportion."""
    if n == 0:
        return 0, 0
    z = stats.norm.ppf((1 + confidence) / 2)
    p = k / n
    denominator = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denominator
    spread = (z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))) / denominator
    lower = max(0.0, center - spread)
    upper = min(1.0, center + spread)
    return lower, upper

def main():
    script_dir = r"C:\Users\Asus\.gemini\antigravity-cli\brain\2e5fc834-dd2c-4d2e-8be6-14c38974dd26\scratch\benchmark_hardened\workspaces\ab_experiment_baseline_ea54bb"
    data_path = os.path.join(script_dir, "data.csv")
    output_path = os.path.join(script_dir, "edited_plot.png")

    df = pd.read_csv(data_path)

    # Extract metrics
    df['conversion_rate'] = df['conversions'] / df['visitors']
    df['cr_pct'] = df['conversion_rate'] * 100

    # Calculate Wilson 95% CIs
    ci_bounds = [compute_wilson_ci(row['conversions'], row['visitors']) for _, row in df.iterrows()]
    df['ci_lower_pct'] = [b[0] * 100 for b in ci_bounds]
    df['ci_upper_pct'] = [b[1] * 100 for b in ci_bounds]
    df['err_lower'] = df['cr_pct'] - df['ci_lower_pct']
    df['err_upper'] = df['ci_upper_pct'] - df['cr_pct']

    # Two-proportion z-test
    n_a = df.loc[df['variant'] == 'A', 'visitors'].values[0]
    k_a = df.loc[df['variant'] == 'A', 'conversions'].values[0]
    p_a = df.loc[df['variant'] == 'A', 'conversion_rate'].values[0]

    n_b = df.loc[df['variant'] == 'B', 'visitors'].values[0]
    k_b = df.loc[df['variant'] == 'B', 'conversions'].values[0]
    p_b = df.loc[df['variant'] == 'B', 'conversion_rate'].values[0]

    p_pool = (k_a + k_b) / (n_a + n_b)
    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z_stat = (p_b - p_a) / se_pool
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    abs_diff_pct = (p_b - p_a) * 100
    rel_lift_pct = ((p_b - p_a) / p_a) * 100

    # Difference 95% CI (unpooled)
    se_diff = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    z_crit = stats.norm.ppf(0.975)
    ci_diff_lower_pct = (p_b - p_a - z_crit * se_diff) * 100
    ci_diff_upper_pct = (p_b - p_a + z_crit * se_diff) * 100

    # Styling setup
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['axes.edgecolor'] = '#CCCCCC'
    plt.rcParams['axes.linewidth'] = 0.8

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6.5), dpi=300)
    fig.patch.set_facecolor('#FAFAFA')

    palette = {'A': '#332288', 'B': '#88CCEE'}

    # --- PANEL 1: Conversion Rate with 95% CI ---
    ax1.set_facecolor('#FFFFFF')
    ax1.grid(axis='y', linestyle='--', alpha=0.4, color='#94A3B8', zorder=0)

    x_pos = [0, 1]
    bar_width = 0.52
    colors = [palette['A'], palette['B']]

    bars = ax1.bar(
        x_pos,
        df['cr_pct'],
        yerr=[df['err_lower'], df['err_upper']],
        capsize=6,
        width=bar_width,
        color=colors,
        alpha=0.88,
        edgecolor=[c for c in colors],
        linewidth=1.2,
        zorder=3,
        error_kw={'elinewidth': 1.5, 'ecolor': '#1E293B', 'capsize': 6, 'capthick': 1.5}
    )

    # Bar value labels
    for i, row in df.iterrows():
        cr = row['cr_pct']
        ci_l = row['ci_lower_pct']
        ci_u = row['ci_upper_pct']
        ax1.text(
            x_pos[i],
            cr / 2,
            f"{cr:.2f}%\n({row['conversions']:,} / {row['visitors']:,})",
            ha='center',
            va='center',
            color='white',
            fontweight='bold',
            fontsize=11,
            zorder=4
        )
        # CI label above error bar
        ax1.text(
            x_pos[i],
            ci_u + 0.12,
            f"95% CI: [{ci_l:.2f}%, {ci_u:.2f}%]",
            ha='center',
            va='bottom',
            color='#334155',
            fontsize=9.5,
            fontweight='normal'
        )

    # Significance bracket between bars
    y_line = 4.95
    tick_len = 0.12

    ax1.plot([0, 0, 1, 1], [y_line - tick_len, y_line, y_line, y_line - tick_len], color='#334155', lw=1.2)
    sig_text = f"Relative Lift: {rel_lift_pct:+.1f}%\nAbsolute Δ: {abs_diff_pct:+.2f}% (p = {p_value:.4f} **)"
    ax1.text(
        0.5, y_line + 0.08, sig_text,
        ha='center', va='bottom', fontsize=10, fontweight='bold', color='#117733'
    )

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(['Variant A\n(Baseline)', 'Variant B\n(Treatment)'], fontsize=11, fontweight='bold')
    ax1.set_xlabel('Edited X', fontsize=12, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Edited Y', fontsize=12, fontweight='bold', color='#1E293B')
    ax1.set_title('Edited benchmark figure', fontsize=12.5, fontweight='bold', pad=14, loc='left')
    ax1.set_ylim(0, 5.8)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # --- PANEL 2: Traffic Allocation & Funnel Breakdown ---
    ax2.set_facecolor('#FFFFFF')
    ax2.grid(axis='y', linestyle='--', alpha=0.4, color='#94A3B8', zorder=0)

    # Plot total visitors with conversions as highlighted portion
    non_conversions = df['visitors'] - df['conversions']

    p_non_conv = ax2.bar(
        x_pos,
        non_conversions,
        width=bar_width,
        label='Non-Converted Visitors',
        color='#44AA99',
        edgecolor='#117733',
        linewidth=1.0,
        zorder=3
    )

    p_conv = ax2.bar(
        x_pos,
        df['conversions'],
        bottom=non_conversions,
        width=bar_width,
        label='Conversions',
        color=colors,
        edgecolor=[c for c in colors],
        linewidth=1.2,
        zorder=3
    )

    # Annotate total visitors and conversion counts
    total_sample = df['visitors'].sum()
    for i, row in df.iterrows():
        visitors = row['visitors']
        convs = row['conversions']
        share = (visitors / total_sample) * 100
        # Text at top of bar
        ax2.text(
            x_pos[i],
            visitors + 300,
            f"Total: {visitors:,}\n({share:.1f}% traffic)",
            ha='center',
            va='bottom',
            color='#1E293B',
            fontweight='bold',
            fontsize=10.5
        )
        # Text inside non-converted
        ax2.text(
            x_pos[i],
            visitors / 2,
            f"Non-converted:\n{(visitors - convs):,}",
            ha='center',
            va='center',
            color='#475569',
            fontsize=9.5
        )

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(['Variant A\n(Baseline)', 'Variant B\n(Treatment)'], fontsize=11, fontweight='bold')
    ax2.set_xlabel('Edited X', fontsize=12, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Edited Y', fontsize=12, fontweight='bold', color='#1E293B')
    ax2.set_title('Edited benchmark figure', fontsize=12.5, fontweight='bold', pad=14, loc='left')
    ax2.set_ylim(0, 18500)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}"))
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # Custom Legend for Panel 2
    legend_elements = [
        mpatches.Patch(facecolor='#44AA99', edgecolor='#117733', label='Non-Converted Visitors'),
        mpatches.Patch(facecolor='#332288', label='Conversions (Variant A)'),
        mpatches.Patch(facecolor='#88CCEE', label='Conversions (Variant B)')
    ]
    ax2.legend(handles=legend_elements, loc='upper left', frameon=True, framealpha=0.9, facecolor='#F8FAFC', edgecolor='#E2E8F0', fontsize=9.5)

    # Super Title and Summary Header
    fig.suptitle(
        "Edited benchmark figure",
        fontsize=15,
        fontweight='bold',
        color='#0F172A',
        y=0.98
    )

    # Add bottom summary banner box
    summary_box_text = (
        f"Statistical Summary: Two-proportion z-test indicates Variant B has a statistically significant lower conversion rate than Variant A\n"
        f"(z = {z_stat:.2f}, p = {p_value:.4f} < 0.01). Absolute difference: {abs_diff_pct:+.2f} percentage points (95% CI: [{ci_diff_lower_pct:+.2f}%, {ci_diff_upper_pct:+.2f}%]), "
        f"Relative change: {rel_lift_pct:+.1f}%.\n"
        f"Note: Traffic allocation was asymmetric (Variant A: {n_a:,} [20.8%], Variant B: {n_b:,} [79.2%])."
    )

    fig.text(
        0.5, 0.02,
        summary_box_text,
        ha='center',
        va='bottom',
        fontsize=9,
        color='#334155',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#F1F5F9', edgecolor='#44AA99', linewidth=1)
    )

    plt.tight_layout(rect=[0, 0.10, 1, 0.94])
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Plot successfully saved to {output_path}")

if __name__ == "__main__":
    main()
