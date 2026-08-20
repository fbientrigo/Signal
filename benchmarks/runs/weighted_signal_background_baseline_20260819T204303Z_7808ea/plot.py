import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------
# Publication Styling Configuration
# ---------------------------------------------------------
plt.rcParams.update({
    'font.size': 10.5,
    'font.family': 'sans-serif',
    'axes.labelsize': 11.5,
    'axes.titlesize': 12.0,
    'xtick.labelsize': 10.0,
    'ytick.labelsize': 10.0,
    'legend.fontsize': 9.5,
    'figure.titlesize': 14.0,
    'figure.dpi': 300,
    'mathtext.fontset': 'cm'
})

# Load Data
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'data.csv')
df = pd.read_csv(data_path)

sig = df[df['sample'] == 'signal'].copy()
bkg = df[df['sample'] == 'background'].copy()

# Colorblind-safe palette (Tol / Okabe-Ito inspired)
c_sig = '#0072B2'        # Deep Blue
c_sig_fill = '#56B4E9'   # Sky Blue
c_bkg = '#D55E00'        # Vermillion / Red-Orange
c_bkg_fill = '#E69F00'   # Orange
c_purity = '#009E73'     # Bluish Green
c_tail_bg = '#FEF3C7'    # Amber tint
c_tail_line = '#D97706'  # Dark amber line

def compute_binned_stats(data, bin_edges):
    """
    Computes weighted yield and independent statistical uncertainty per bin.
    Yield: Y = sum(w_i)
    Uncertainty: sigma = sqrt(sum(w_i^2))
    """
    n_bins = len(bin_edges) - 1
    yields = np.zeros(n_bins)
    errors = np.zeros(n_bins)
    counts = np.zeros(n_bins, dtype=int)
    
    for i in range(n_bins):
        low, high = bin_edges[i], bin_edges[i+1]
        if i == n_bins - 1:
            mask = (data['score'] >= low) & (data['score'] <= high)
        else:
            mask = (data['score'] >= low) & (data['score'] < high)
        weights = data.loc[mask, 'weight'].values
        yields[i] = np.sum(weights)
        errors[i] = np.sqrt(np.sum(weights**2))
        counts[i] = len(weights)
        
    return yields, errors, counts

# Overall Statistics
tot_sig_yield = sig['weight'].sum()
tot_sig_err = np.sqrt((sig['weight']**2).sum())
tot_bkg_yield = bkg['weight'].sum()
tot_bkg_err = np.sqrt((bkg['weight']**2).sum())

# Tail Statistics (Score >= 0.8)
sig_tail = sig[sig['score'] >= 0.8]
bkg_tail = bkg[bkg['score'] >= 0.8]
tail_sig_yield = sig_tail['weight'].sum()
tail_sig_err = np.sqrt((sig_tail['weight']**2).sum())
tail_bkg_yield = bkg_tail['weight'].sum()
tail_bkg_err = np.sqrt((bkg_tail['weight']**2).sum())

tail_sb = tail_sig_yield / tail_bkg_yield
tail_purity = tail_sig_yield / (tail_sig_yield + tail_bkg_yield)
sig_eff = tail_sig_yield / tot_sig_yield
bkg_rejection = 1.0 - (tail_bkg_yield / tot_bkg_yield)

# Create 3-Panel Figure
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.6), gridspec_kw={'width_ratios': [1.15, 1.0, 1.05]})

# =========================================================================
# Panel (a): Full Score Spectrum (0.0 to 1.0)
# =========================================================================
bins_full = np.linspace(0.0, 1.0, 11)
centers_full = 0.5 * (bins_full[:-1] + bins_full[1:])
width_full = 0.1

sig_y_full, sig_e_full, _ = compute_binned_stats(sig, bins_full)
bkg_y_full, bkg_e_full, _ = compute_binned_stats(bkg, bins_full)

# Highlight Tail Region (Score >= 0.8)
ax1.axvspan(0.8, 1.0, color=c_tail_bg, alpha=0.8, zorder=1, label='Tail Region (Score $\\geq 0.8$)')
ax1.axvline(0.8, color=c_tail_line, linestyle='--', linewidth=1.6, zorder=2)

# Background distribution
ax1.bar(centers_full, bkg_y_full, width=width_full, color=c_bkg_fill, alpha=0.35,
        edgecolor=c_bkg, linewidth=1.4, zorder=3)
ax1.errorbar(centers_full, bkg_y_full, yerr=bkg_e_full, fmt='o', color=c_bkg,
             markersize=5, capsize=3.5, capthick=1.2, elinewidth=1.2, zorder=4,
             label=f'Background (Yield = {tot_bkg_yield:.2f} $\\pm$ {tot_bkg_err:.2f})')

# Signal distribution
ax1.bar(centers_full, sig_y_full, width=width_full, color=c_sig_fill, alpha=0.35,
        edgecolor=c_sig, linewidth=1.4, zorder=3)
ax1.errorbar(centers_full, sig_y_full, yerr=sig_e_full, fmt='s', color=c_sig,
             markersize=5, capsize=3.5, capthick=1.2, elinewidth=1.2, zorder=4,
             label=f'Signal (Yield = {tot_sig_yield:.2f} $\\pm$ {tot_sig_err:.2f})')

# Individual event rug plot
y_bkg_rug = -0.22
y_sig_rug = -0.48
ax1.scatter(bkg['score'], [y_bkg_rug]*len(bkg), marker='|', color=c_bkg, s=65, linewidths=1.5, zorder=5)
ax1.scatter(sig['score'], [y_sig_rug]*len(sig), marker='|', color=c_sig, s=65, linewidths=1.5, zorder=5)
ax1.text(0.01, y_bkg_rug, 'Bkg events', color=c_bkg, fontsize=8.0, verticalalignment='center', fontweight='bold')
ax1.text(0.01, y_sig_rug, 'Sig events', color=c_sig, fontsize=8.0, verticalalignment='center', fontweight='bold')

ax1.set_xlabel('Classifier Score', fontweight='bold')
ax1.set_ylabel('Expected Yield / 0.1 Score Bin', fontweight='bold')
ax1.set_title('(a) Full Classifier Score Spectrum', fontweight='bold', pad=9)
ax1.set_xlim(-0.02, 1.02)
ax1.set_ylim(-0.70, 5.5)
ax1.set_xticks(np.arange(0.0, 1.05, 0.2))
ax1.grid(True, linestyle=':', alpha=0.6, zorder=0)
ax1.legend(loc='upper left', frameon=True, framealpha=0.95, edgecolor='#cccccc', fontsize=9.0)

# =========================================================================
# Panel (b): Signal-Enriched Tail Detail (0.8 to 1.0)
# =========================================================================
bins_tail = np.linspace(0.8, 1.0, 5) # 4 bins: [0.80, 0.85], [0.85, 0.90], [0.90, 0.95], [0.95, 1.00]
centers_tail = 0.5 * (bins_tail[:-1] + bins_tail[1:])
width_tail = 0.05

sig_y_tail, sig_e_tail, _ = compute_binned_stats(sig, bins_tail)
bkg_y_tail, bkg_e_tail, _ = compute_binned_stats(bkg, bins_tail)

# Background bars & errors in tail
ax2.bar(centers_tail, bkg_y_tail, width=width_tail, color=c_bkg_fill, alpha=0.35,
        edgecolor=c_bkg, linewidth=1.4, zorder=3,
        label=f'Background ({tail_bkg_yield:.2f} $\\pm$ {tail_bkg_err:.2f})')
ax2.errorbar(centers_tail, bkg_y_tail, yerr=bkg_e_tail, fmt='o', color=c_bkg,
             markersize=5, capsize=4, capthick=1.2, elinewidth=1.2, zorder=4)

# Signal bars & errors in tail
ax2.bar(centers_tail, sig_y_tail, width=width_tail, color=c_sig_fill, alpha=0.35,
        edgecolor=c_sig, linewidth=1.4, zorder=3,
        label=f'Signal ({tail_sig_yield:.2f} $\\pm$ {tail_sig_err:.2f})')
ax2.errorbar(centers_tail, sig_y_tail, yerr=sig_e_tail, fmt='s', color=c_sig,
             markersize=5, capsize=4, capthick=1.2, elinewidth=1.2, zorder=4)

# Event markers and weights in tail
y_bkg_t = -0.16
y_sig_t = -0.36
ax2.scatter(bkg_tail['score'], [y_bkg_t]*len(bkg_tail), marker='|', color=c_bkg, s=75, linewidths=1.6, zorder=5)
ax2.scatter(sig_tail['score'], [y_sig_t]*len(sig_tail), marker='|', color=c_sig, s=75, linewidths=1.6, zorder=5)
ax2.text(0.795, y_bkg_t, 'Bkg', color=c_bkg, fontsize=8.0, verticalalignment='center', fontweight='bold')
ax2.text(0.795, y_sig_t, 'Sig', color=c_sig, fontsize=8.0, verticalalignment='center', fontweight='bold')

for _, r in sig_tail.iterrows():
    ax2.annotate(f"w={r['weight']:.1f}", (r['score'], y_sig_t - 0.15), ha='center', fontsize=7.5, color=c_sig, fontweight='bold')
for _, r in bkg_tail.iterrows():
    ax2.annotate(f"w={r['weight']:.2f}", (r['score'], y_bkg_t + 0.13), ha='center', fontsize=7.5, color=c_bkg, fontweight='bold')

# Tail summary metrics text box
summary_box = (
    r"$\mathbf{Tail\ Metrics\ (Score \geq 0.8):}$" + "\n"
    r"$\bullet\ S/B\ \mathrm{Ratio}: " + f"{tail_sb:.2f}$\n"
    r"$\bullet\ \mathrm{Purity}\ S/(S+B): " + f"{tail_purity*100:.1f}\\%$\n"
    r"$\bullet\ \mathrm{Sig\ Retained}: " + f"{sig_eff*100:.1f}\\%$\n"
    r"$\bullet\ \mathrm{Bkg\ Rejected}: " + f"{bkg_rejection*100:.1f}\\%$"
)
ax2.text(0.04, 0.96, summary_box, transform=ax2.transAxes, verticalalignment='top',
         fontsize=8.8, linespacing=1.35,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC', alpha=0.95, edgecolor='#94A3B8', linewidth=1.1))

ax2.set_xlabel('Classifier Score (Tail Detail)', fontweight='bold')
ax2.set_ylabel('Expected Yield / 0.05 Score Bin', fontweight='bold')
ax2.set_title('(b) Tail Signal Region Detail (Score $\\geq 0.8$)', fontweight='bold', pad=9)
ax2.set_xlim(0.79, 1.01)
ax2.set_ylim(-0.62, 3.4)
ax2.set_xticks(np.arange(0.80, 1.01, 0.05))
ax2.grid(True, linestyle=':', alpha=0.6, zorder=0)
ax2.legend(loc='upper right', frameon=True, framealpha=0.95, edgecolor='#cccccc', fontsize=9.0)

# =========================================================================
# Panel (c): Cumulative Yield & Selection Purity vs Score Threshold
# =========================================================================
thresholds = np.linspace(0.0, 0.96, 300)
cum_sig = np.array([sig[sig['score'] >= t]['weight'].sum() for t in thresholds])
cum_bkg = np.array([bkg[bkg['score'] >= t]['weight'].sum() for t in thresholds])
cum_purity = np.where((cum_sig + cum_bkg) > 0, cum_sig / (cum_sig + cum_bkg) * 100.0, 0.0)

ax3.axvspan(0.8, 1.0, color=c_tail_bg, alpha=0.8, zorder=0)
ax3.axvline(0.8, color=c_tail_line, linestyle='--', linewidth=1.6, zorder=1)

p1 = ax3.plot(thresholds, cum_sig, color=c_sig, linewidth=2.2, label='Cumulative Signal Yield ($Y_S$)')
p2 = ax3.plot(thresholds, cum_bkg, color=c_bkg, linewidth=2.2, linestyle='--', label='Cumulative Bkg Yield ($Y_B$)')

# Twin axis for Signal Purity
ax3_twin = ax3.twinx()
p3 = ax3_twin.plot(thresholds, cum_purity, color=c_purity, linewidth=2.0, linestyle=':', label='Signal Purity $S/(S+B)$')

# Marker at threshold = 0.8
ax3.plot([0.8], [tail_sig_yield], 's', color=c_sig, markersize=6, zorder=6)
ax3.plot([0.8], [tail_bkg_yield], 'o', color=c_bkg, markersize=6, zorder=6)
ax3_twin.plot([0.8], [tail_purity * 100.0], '^', color=c_purity, markersize=6, zorder=6)

ax3.set_xlabel('Cut Threshold on Score ($x_{\\mathrm{cut}}$)', fontweight='bold')
ax3.set_ylabel('Cumulative Expected Yield ($Score \\geq x_{\\mathrm{cut}}$)', fontweight='bold')
ax3_twin.set_ylabel('Signal Purity [%]', color=c_purity, fontweight='bold')
ax3_twin.tick_params(axis='y', labelcolor=c_purity)
ax3_twin.set_ylim(0, 105)
ax3.set_xlim(0.0, 1.0)
ax3.set_ylim(0, 17.5)
ax3.set_title('(c) Cumulative Yield & Purity vs Cut Threshold', fontweight='bold', pad=9)
ax3.grid(True, linestyle=':', alpha=0.6)

# Combined Legend for panel (c)
lines = p1 + p2 + p3
labels = [l.get_label() for l in lines]
ax3.legend(lines, labels, loc='center left', frameon=True, framealpha=0.95, edgecolor='#cccccc', fontsize=8.8)

# Overall Figure Title
plt.suptitle('Weighted Signal vs. Background Score Spectrum and High-Score Tail Region Analysis',
             fontsize=13.5, fontweight='bold', y=0.99)
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save Output
output_path = os.path.join(script_dir, 'plot.png')
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Successfully generated {output_path}")
