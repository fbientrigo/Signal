import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

def main():
    work_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(work_dir, 'data.csv')
    df = pd.read_csv(data_path)
    
    sig_df = df[df['sample'] == 'signal'].copy()
    bkg_df = df[df['sample'] == 'background'].copy()
    
    # 10 bins of width 0.1 across score range [0.0, 1.0]
    n_bins = 10
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_width = bin_edges[1] - bin_edges[0]
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    
    # Weighted yield and independent statistical uncertainty per bin
    # Yield Y = sum(w_i)
    # Variance Var(Y) = sum(w_i^2)
    # Stat uncertainty sigma = sqrt(sum(w_i^2))
    def compute_binned_stats(sample_df):
        yields = np.zeros(n_bins)
        errors = np.zeros(n_bins)
        
        for i in range(n_bins):
            low, high = bin_edges[i], bin_edges[i+1]
            if i == n_bins - 1:
                mask = (sample_df['score'] >= low) & (sample_df['score'] <= high)
            else:
                mask = (sample_df['score'] >= low) & (sample_df['score'] < high)
            
            w = sample_df.loc[mask, 'weight'].values
            if len(w) > 0:
                yields[i] = np.sum(w)
                errors[i] = np.sqrt(np.sum(w**2))
            else:
                yields[i] = 0.0
                errors[i] = 0.0
        return yields, errors

    sig_yields, sig_errors = compute_binned_stats(sig_df)
    bkg_yields, bkg_errors = compute_binned_stats(bkg_df)
    
    tot_sig = np.sum(sig_df['weight'])
    tot_sig_err = np.sqrt(np.sum(sig_df['weight']**2))
    tot_bkg = np.sum(bkg_df['weight'])
    tot_bkg_err = np.sqrt(np.sum(bkg_df['weight']**2))
    
    tail_sig_mask = sig_df['score'] >= 0.8
    tail_bkg_mask = bkg_df['score'] >= 0.8
    
    tail_sig = np.sum(sig_df.loc[tail_sig_mask, 'weight'])
    tail_sig_err = np.sqrt(np.sum(sig_df.loc[tail_sig_mask, 'weight']**2))
    tail_bkg = np.sum(bkg_df.loc[tail_bkg_mask, 'weight'])
    tail_bkg_err = np.sqrt(np.sum(bkg_df.loc[tail_bkg_mask, 'weight']**2))
    
    tail_sb = tail_sig / tail_bkg if tail_bkg > 0 else np.nan
    tail_sb_err = tail_sb * np.sqrt((tail_sig_err / tail_sig)**2 + (tail_bkg_err / tail_bkg)**2) if tail_bkg > 0 else np.nan
    
    tail_purity = tail_sig / (tail_sig + tail_bkg) if (tail_sig + tail_bkg) > 0 else np.nan
    tail_purity_err = np.sqrt((tail_bkg**2 * tail_sig_err**2 + tail_sig**2 * tail_bkg_err**2)) / ((tail_sig + tail_bkg)**2)
    
    overall_purity = tot_sig / (tot_sig + tot_bkg)
    overall_sb = tot_sig / tot_bkg
    
    # Bin-by-bin purity: P = S / (S + B) and propagated uncertainty
    purities = np.zeros(n_bins)
    purity_errors = np.zeros(n_bins)
    
    for i in range(n_bins):
        s, s_err = sig_yields[i], sig_errors[i]
        b, b_err = bkg_yields[i], bkg_errors[i]
        tot = s + b
        if tot > 0:
            purities[i] = s / tot
            purity_errors[i] = np.sqrt(b**2 * s_err**2 + s**2 * b_err**2) / (tot**2)
        else:
            purities[i] = 0.0
            purity_errors[i] = 0.0

    # Cumulative yields as a function of score cut s_cut
    cut_grid = np.linspace(0.0, 1.0, 101)
    sig_cum = np.zeros(len(cut_grid))
    sig_cum_err = np.zeros(len(cut_grid))
    bkg_cum = np.zeros(len(cut_grid))
    bkg_cum_err = np.zeros(len(cut_grid))
    
    for idx, cut in enumerate(cut_grid):
        s_w = sig_df.loc[sig_df['score'] >= cut, 'weight'].values
        b_w = bkg_df.loc[bkg_df['score'] >= cut, 'weight'].values
        
        s_val = np.sum(s_w) if len(s_w) > 0 else 0.0
        s_err = np.sqrt(np.sum(s_w**2)) if len(s_w) > 0 else 0.0
        b_val = np.sum(b_w) if len(b_w) > 0 else 0.0
        b_err = np.sqrt(np.sum(b_w**2)) if len(b_w) > 0 else 0.0
        
        sig_cum[idx] = s_val
        sig_cum_err[idx] = s_err
        bkg_cum[idx] = b_val
        bkg_cum_err[idx] = b_err

    # Plot styling
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 10.5,
        'axes.labelsize': 11.5,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 9.0,
        'figure.titlesize': 13.5,
        'mathtext.fontset': 'dejavusans'
    })
    
    fig = plt.figure(figsize=(13.6, 7.0))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.22, 1.0], height_ratios=[2.7, 1.2], hspace=0.10, wspace=0.22)
    
    ax_main = fig.add_subplot(gs[0, 0])
    ax_ratio = fig.add_subplot(gs[1, 0], sharex=ax_main)
    ax_card = fig.add_subplot(gs[0, 1])
    ax_cum = fig.add_subplot(gs[1, 1])
    
    color_sig = '#332288'      # Deep Royal Blue
    color_sig_light = '#88CCEE'
    color_bkg = '#44AA99'      # Vermilion
    color_bkg_light = '#117733'
    color_tail = '#999933'     # Green highlight
    color_tail_bg = '#DDCC77'
    
    # -------------------------------------------------------------
    # 1. Panel (a): Differential Yields vs Score
    # -------------------------------------------------------------
    ax_main.axvspan(0.8, 1.0, color=color_tail_bg, alpha=0.9, zorder=1)
    ax_main.axvline(0.8, color=color_tail, linestyle='--', linewidth=1.8, alpha=0.85, zorder=4)
    
    # Step histograms
    ax_main.stairs(sig_yields, bin_edges, color=color_sig, linewidth=2.2, zorder=3)
    ax_main.stairs(bkg_yields, bin_edges, color=color_bkg, linewidth=2.2, zorder=3)
    
    # Statistical uncertainty bands (shaded bars)
    ax_main.bar(
        bin_centers, 2 * sig_errors, width=bin_width, 
        bottom=np.maximum(0, sig_yields - sig_errors), 
        color=color_sig_light, alpha=0.45, edgecolor='none', zorder=2
    )
    ax_main.bar(
        bin_centers, 2 * bkg_errors, width=bin_width, 
        bottom=np.maximum(0, bkg_yields - bkg_errors), 
        color=color_bkg_light, alpha=0.45, edgecolor='none', zorder=2
    )
    
    # Error bars at bin centers
    ax_main.errorbar(
        bin_centers - 0.006, sig_yields, yerr=sig_errors, fmt='o', 
        color=color_sig, markersize=5.5, capsize=3.5, capthick=1.2, 
        elinewidth=1.4, zorder=5
    )
    ax_main.errorbar(
        bin_centers + 0.006, bkg_yields, yerr=bkg_errors, fmt='s', 
        color=color_bkg, markersize=5.0, capsize=3.5, capthick=1.2, 
        elinewidth=1.4, zorder=5
    )
    
    # Tail annotation badge
    ax_main.text(
        0.90, 5.0, 'Signal-Rich Tail\n(Score $\\geq 0.8$)', 
        fontsize=9.5, fontweight='bold', color='#117733', ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#E8F5E9', edgecolor='#2CA02C', alpha=0.95, linewidth=1.2),
        zorder=7
    )
    
    # Legend in main axis
    legend_elements_main = [
        Line2D([0], [0], color=color_sig, lw=2.2, marker='o', markersize=5, label=f'Signal ($N_{{\\mathrm{{exp}}}} = {tot_sig:.2f} \\pm {tot_sig_err:.2f}$)'),
        Line2D([0], [0], color=color_bkg, lw=2.2, marker='s', markersize=5, label=f'Background ($N_{{\\mathrm{{exp}}}} = {tot_bkg:.2f} \\pm {tot_bkg_err:.2f}$)'),
        Patch(facecolor='#888888', alpha=0.4, edgecolor='none', label=r'Stat. Uncertainty ($\pm 1\sigma = \sqrt{\sum w_i^2}$)'),
    ]
    ax_main.legend(
        handles=legend_elements_main, loc='upper left',
        frameon=True, facecolor='white', framealpha=0.95, edgecolor='#CCCCCC', fontsize=8.8
    )
    
    ax_main.set_ylabel('Edited Y', fontweight='bold')
    ax_main.set_ylim(0, 5.5)
    ax_main.set_xlim(0.0, 1.0)
    ax_main.grid(True, linestyle='--', alpha=0.45, zorder=0)
    ax_main.set_title('Edited benchmark figure', fontweight='bold', loc='left', pad=8)
    
    # -------------------------------------------------------------
    # 2. Panel (b): Signal Purity per Bin
    # -------------------------------------------------------------
    ax_ratio.axvspan(0.8, 1.0, color=color_tail_bg, alpha=0.9, zorder=1)
    ax_ratio.axvline(0.8, color=color_tail, linestyle='--', linewidth=1.8, alpha=0.85, zorder=4)
    
    ax_ratio.axhline(0.5, color='#888888', linestyle=':', linewidth=1.2, zorder=2, label='Equal Yield ($S = B, 50\%$)')
    ax_ratio.axhline(overall_purity, color='#6A1B9A', linestyle='-.', linewidth=1.2, alpha=0.85, zorder=2, label=f'Baseline Purity ({overall_purity*100:.1f}%)')
    
    ax_ratio.errorbar(
        bin_centers, purities, yerr=purity_errors, fmt='D-', 
        color='#332288', markerfacecolor=color_sig, markeredgecolor='#332288',
        markersize=5.5, capsize=3.5, capthick=1.2, elinewidth=1.4, linewidth=1.5,
        zorder=5, label=r'Bin Purity $\pm 1\sigma_{\mathrm{stat}}$'
    )
    ax_ratio.fill_between(
        bin_centers, 
        np.maximum(0, purities - purity_errors), 
        np.minimum(1, purities + purity_errors), 
        color=color_sig_light, alpha=0.35, zorder=3
    )
    
    ax_ratio.set_xlabel('Edited X', fontweight='bold')
    ax_ratio.set_ylabel('Signal Purity\n$S / (S + B)$', fontweight='bold')
    ax_ratio.set_ylim(-0.05, 1.08)
    ax_ratio.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax_ratio.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0, decimals=0))
    ax_ratio.grid(True, linestyle='--', alpha=0.45, zorder=0)
    ax_ratio.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.92, edgecolor='#CCCCCC', fontsize=8.2, handletextpad=0.4)
    
    # -------------------------------------------------------------
    # 3. Panel (c): Scientific Summary Metrics Card (Table)
    # -------------------------------------------------------------
    ax_card.axis('off')
    
    summary_rows = [
        ["Full Sample Metric", "Signal (S)", "Background (B)", "Summary / Ratio"],
        ["Raw Events (N)", f"{len(sig_df)}", f"{len(bkg_df)}", f"{len(df)} Total"],
        ["Total Weighted Yield", f"{tot_sig:.2f} ± {tot_sig_err:.2f}", f"{tot_bkg:.2f} ± {tot_bkg_err:.2f}", f"S/B = {overall_sb:.2f}"],
        ["Overall Signal Purity", "-", "-", f"{overall_purity*100:.1f}%"],
        ["Tail Region (Score ≥ 0.8)", "Signal (S)", "Background (B)", "Tail Enrichment"],
        ["Tail Weighted Yield", f"{tail_sig:.2f} ± {tail_sig_err:.2f}", f"{tail_bkg:.2f} ± {tail_bkg_err:.2f}", f"Tail S/B = {tail_sb:.2f} ± {tail_sb_err:.2f}"],
        ["Fraction in Tail (≥ 0.8)", f"{tail_sig/tot_sig*100:.1f}%", f"{tail_bkg/tot_bkg*100:.1f}%", f"Bkg Rejection = {100 - tail_bkg/tot_bkg*100:.1f}%"],
        ["Tail Signal Purity", "-", "-", f"{tail_purity*100:.1f}% ± {tail_purity_err*100:.1f}%"],
        ["Enrichment Factor", "-", "-", f"{(tail_sb / overall_sb):.1f}× increase in S/B"],
    ]
    
    col_widths = [0.34, 0.22, 0.22, 0.22]
    table = ax_card.table(
        cellText=summary_rows,
        colWidths=col_widths,
        cellLoc='center',
        bbox=[0.0, 0.02, 1.0, 0.88]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    
    # Styling table cells
    for (row_idx, col_idx), cell in table.get_celld().items():
        cell.set_edgecolor('#D0D7DE')
        cell.set_linewidth(0.8)
        if row_idx == 0 or row_idx == 4:
            cell.set_facecolor('#EAEFF5')
            cell.set_text_props(weight='bold', color='#0F2942')
        elif row_idx in [5, 6, 7, 8]:
            cell.set_facecolor('#F6FAF6')
            if col_idx == 3:
                cell.set_text_props(weight='bold', color='#117733')
        else:
            cell.set_facecolor('#FFFFFF')
    
    ax_card.set_title('Edited benchmark figure', fontweight='bold', loc='left', pad=8)
    
    # -------------------------------------------------------------
    # 4. Panel (d): Cumulative Yield & Efficiency vs Score Cut
    # -------------------------------------------------------------
    ax_cum.axvspan(0.8, 1.0, color=color_tail_bg, alpha=0.9, zorder=1)
    ax_cum.axvline(0.8, color=color_tail, linestyle='--', linewidth=1.8, alpha=0.85, zorder=4)
    
    ax_cum.plot(cut_grid, sig_cum, color=color_sig, lw=2.0, label=f'Signal Yield $Y_S(\\geq s)$', zorder=3)
    ax_cum.fill_between(
        cut_grid, 
        np.maximum(0, sig_cum - sig_cum_err), 
        sig_cum + sig_cum_err, 
        color=color_sig_light, alpha=0.35, zorder=2
    )
    
    ax_cum.plot(cut_grid, bkg_cum, color=color_bkg, lw=2.0, label=f'Bkg Yield $Y_B(\\geq s)$', zorder=3)
    ax_cum.fill_between(
        cut_grid, 
        np.maximum(0, bkg_cum - bkg_cum_err), 
        bkg_cum + bkg_cum_err, 
        color=color_bkg_light, alpha=0.35, zorder=2
    )
    
    # Mark the 0.8 cut point
    ax_cum.scatter([0.8], [tail_sig], color=color_sig, s=40, zorder=6)
    ax_cum.scatter([0.8], [tail_bkg], color=color_bkg, s=40, zorder=6)
    
    ax_cum.text(
        0.81, 11.8, f"Cut at 0.8:\nS = {tail_sig:.1f} ({tail_sig/tot_sig*100:.0f}%)\nB = {tail_bkg:.1f} ({tail_bkg/tot_bkg*100:.1f}%)",
        fontsize=8.5, color='#117733', fontweight='bold', va='top',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#F6FAF6', edgecolor='#2CA02C', alpha=0.9, linewidth=0.8)
    )
    
    ax_cum.set_xlabel('Score Threshold Cut ($s_{\\mathrm{cut}}$)', fontweight='bold')
    ax_cum.set_ylabel('Cumulative Yield\n$Y(\\mathrm{Score} \\geq s_{\\mathrm{cut}})$', fontweight='bold')
    ax_cum.set_xlim(0.0, 1.0)
    ax_cum.set_ylim(0, 17.5)
    ax_cum.grid(True, linestyle='--', alpha=0.45, zorder=0)
    ax_cum.legend(loc='center left', frameon=True, facecolor='white', framealpha=0.92, edgecolor='#CCCCCC', fontsize=8.5)
    ax_cum.set_title('Edited benchmark figure', fontweight='bold', loc='left', pad=8)
    
    # Formatting ticks for all axes
    for ax in (ax_main, ax_ratio, ax_cum):
        ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.05))
    
    fig.subplots_adjust(left=0.065, right=0.975, top=0.92, bottom=0.09, hspace=0.10, wspace=0.22)
    
    output_png = os.path.join(work_dir, 'edited_plot.png')
    fig.savefig(output_png, dpi=300)
    plt.close(fig)
    print(f"Successfully generated {output_png}")
    print(f"Total Signal Yield: {tot_sig:.2f} +/- {tot_sig_err:.2f}")
    print(f"Total Background Yield: {tot_bkg:.2f} +/- {tot_bkg_err:.2f}")
    print(f"Tail (>= 0.8) Signal Yield: {tail_sig:.2f} +/- {tail_sig_err:.2f} ({tail_sig/tot_sig*100:.1f}%)")
    print(f"Tail (>= 0.8) Background Yield: {tail_bkg:.2f} +/- {tail_bkg_err:.2f} ({tail_bkg/tot_bkg*100:.1f}%)")
    print(f"Tail S/B: {tail_sb:.2f} +/- {tail_sb_err:.2f}")
    print(f"Tail Signal Purity: {tail_purity*100:.1f}% +/- {tail_purity_err*100:.1f}%")

if __name__ == '__main__':
    main()
