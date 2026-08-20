import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Load Data
# ---------------------------------------------------------
df = pd.read_csv('data.csv')

sig = df[df['sample'] == 'signal']
bkg = df[df['sample'] == 'background']

# ---------------------------------------------------------
# 2. Binning and Weighted Yield Calculations
# ---------------------------------------------------------
# 10 uniform bins across [0.0, 1.0] with score = 0.8 as an exact boundary
bins = np.linspace(0.0, 1.0, 11)
bin_centers = 0.5 * (bins[:-1] + bins[1:])
bin_width = bins[1] - bins[0]

# Weighted yield: sum(w_i)
# Statistical uncertainty (independent events, fixed weights): sigma = sqrt(sum(w_i^2))
sig_yield, _ = np.histogram(sig['score'], bins=bins, weights=sig['weight'])
sig_var, _ = np.histogram(sig['score'], bins=bins, weights=sig['weight']**2)
sig_err = np.sqrt(sig_var)

bkg_yield, _ = np.histogram(bkg['score'], bins=bins, weights=bkg['weight'])
bkg_var, _ = np.histogram(bkg['score'], bins=bins, weights=bkg['weight']**2)
bkg_err = np.sqrt(bkg_var)

# Full-sample totals
sig_tot_yield = sig['weight'].sum()
sig_tot_err = np.sqrt((sig['weight']**2).sum())
bkg_tot_yield = bkg['weight'].sum()
bkg_tot_err = np.sqrt((bkg['weight']**2).sum())

# Tail region (Score >= 0.8) statistics
sig_tail = sig[sig['score'] >= 0.8]
bkg_tail = bkg[bkg['score'] >= 0.8]
sig_tail_yield = sig_tail['weight'].sum()
sig_tail_err = np.sqrt((sig_tail['weight']**2).sum())
bkg_tail_yield = bkg_tail['weight'].sum()
bkg_tail_err = np.sqrt((bkg_tail['weight']**2).sum())
tail_s_over_b = sig_tail_yield / bkg_tail_yield

# ---------------------------------------------------------
# 3. Figure & Axis Styling (Paper Profile)
# ---------------------------------------------------------
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 10,
    'font.family': 'sans-serif',
})

fig, ax = plt.subplots(figsize=(8.2, 5.5), dpi=300)

# Color scheme (publication-grade, high contrast)
c_sig = '#1f77b4'       # Steel blue
c_sig_dark = '#0d47a1'
c_bkg = '#d95f02'       # Vermilion
c_bkg_dark = '#b34700'
c_tail_bg = '#e8f5e9'   # Pale green highlight
c_tail_line = '#2e7d32'

# ---------------------------------------------------------
# 4. Plot Elements
# ---------------------------------------------------------
# Tail region highlight (Score >= 0.8)
tail_patch = ax.axvspan(0.8, 1.0, color=c_tail_bg, alpha=0.7, zorder=1, label='Tail Region (Score ≥ 0.8)')
ax.axvline(0.8, color=c_tail_line, linestyle='--', linewidth=1.5, alpha=0.9, zorder=2)

# Step histograms with subtle shading
sig_stairs = ax.stairs(sig_yield, bins, color=c_sig, linewidth=2.0, fill=True, alpha=0.14,
                       label=f'Signal (Yield = {sig_tot_yield:.2f} ± {sig_tot_err:.2f})', zorder=3)
ax.stairs(sig_yield, bins, color=c_sig, linewidth=2.0, zorder=4)

bkg_stairs = ax.stairs(bkg_yield, bins, color=c_bkg, linewidth=2.0, fill=True, alpha=0.14,
                       label=f'Background (Yield = {bkg_tot_yield:.2f} ± {bkg_tot_err:.2f})', zorder=3)
ax.stairs(bkg_yield, bins, color=c_bkg, linewidth=2.0, zorder=4)

# Error bars with points (slight horizontal shift to avoid overlap at identical bin centers)
shift = 0.007
mask_bkg = bkg_yield > 0
mask_sig = sig_yield > 0

ax.errorbar(bin_centers[mask_bkg] - shift, bkg_yield[mask_bkg], yerr=bkg_err[mask_bkg],
            fmt='o', markersize=4.5, color=c_bkg_dark, ecolor=c_bkg_dark,
            elinewidth=1.4, capsize=3.0, capthick=1.2, zorder=5)

ax.errorbar(bin_centers[mask_sig] + shift, sig_yield[mask_sig], yerr=sig_err[mask_sig],
            fmt='s', markersize=4.5, color=c_sig_dark, ecolor=c_sig_dark,
            elinewidth=1.4, capsize=3.0, capthick=1.2, zorder=5)

# ---------------------------------------------------------
# 5. Annotations & Notes
# ---------------------------------------------------------
# Tail region summary box
tail_box_text = (
    "Tail Region (Score ≥ 0.8)\n"
    f"• Signal: {sig_tail_yield:.2f} ± {sig_tail_err:.2f}\n"
    f"• Background: {bkg_tail_yield:.2f} ± {bkg_tail_err:.2f}\n"
    f"• S / B Ratio: {tail_s_over_b:.2f}"
)
ax.text(0.90, 7.15, tail_box_text, transform=ax.transData,
        fontsize=9.5, horizontalalignment='center', verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor=c_tail_line, alpha=0.95, linewidth=1.2),
        zorder=6)

# Method note for statistical uncertainties
ax.text(0.03, 0.95, "Statistical uncertainty: σ = √(Σ wᵢ²) per bin (independent fixed weights)",
        transform=ax.transAxes, fontsize=9.0, color='#444444', verticalalignment='top', fontstyle='italic')

# ---------------------------------------------------------
# 6. Axes, Limits, Grid, and Legend
# ---------------------------------------------------------
ax.set_xlim(0.0, 1.0)
ax.set_ylim(0.0, 7.5)
ax.set_xlabel('Classifier Score')
ax.set_ylabel(f'Expected Yield / {bin_width:.1f} Score Bin')
ax.set_title('Signal vs. Background Score Distributions\n(Weighted Yield per Target Exposure)', pad=12)

# Ensure preferred legend order: Signal, Background, Tail Region
handles = [sig_stairs, bkg_stairs, tail_patch]
labels = [h.get_label() for h in handles]
ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(0.03, 0.89), frameon=True, framealpha=0.94, edgecolor='#cccccc')

ax.grid(axis='y', linestyle=':', alpha=0.5, color='#b0b0b0')
ax.set_axisbelow(True)
ax.tick_params(direction='in', which='both', top=True, right=True)

# ---------------------------------------------------------
# 7. Save Figure
# ---------------------------------------------------------
plt.tight_layout()
fig.savefig('plot.png', dpi=300)
plt.close(fig)
