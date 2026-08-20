import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D

# 1. Load data
df = pd.read_csv('data.csv')

# Ensure correct data types
df['mass_gev'] = df['mass_gev'].astype(float)
df['lifetime_mm'] = df['lifetime_mm'].astype(float)
df['efficiency'] = df['efficiency'].astype(float)
if df['excluded'].dtype == object:
    df['excluded'] = df['excluded'].astype(str).str.strip().str.lower() == 'true'
else:
    df['excluded'] = df['excluded'].astype(bool)

# 2. Configure publication typography and styling
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9.5,
    'figure.titlesize': 13,
    'mathtext.fontset': 'dejavusans',
})

fig, ax = plt.subplots(figsize=(7.5, 5.4), dpi=300)

# Colormap and normalization for selection efficiency
cmap = plt.cm.viridis
norm = Normalize(vmin=0.0, vmax=0.20)

# Split allowed vs excluded subsets
allowed = df[~df['excluded']]
excluded = df[df['excluded']]

# 3. Plot allowed evaluated points (solid circles)
sc_allowed = ax.scatter(
    allowed['mass_gev'],
    allowed['lifetime_mm'],
    c=allowed['efficiency'],
    cmap=cmap,
    norm=norm,
    s=230,
    marker='o',
    edgecolors='#1e293b',
    linewidths=1.5,
    zorder=4,
    label='Theory allowed'
)

# 4. Plot excluded evaluated points (squares with red boundary and hatch)
sc_excluded = ax.scatter(
    excluded['mass_gev'],
    excluded['lifetime_mm'],
    c=excluded['efficiency'],
    cmap=cmap,
    norm=norm,
    s=250,
    marker='s',
    edgecolors='#dc2626',
    linewidths=2.0,
    hatch='//',
    zorder=4,
    label='Excluded by theory'
)

# Overlay red cross on excluded points for clear print/monochrome distinction
ax.scatter(
    excluded['mass_gev'],
    excluded['lifetime_mm'],
    color='#dc2626',
    s=75,
    marker='x',
    linewidths=1.8,
    zorder=5
)

# 5. Numerical annotations for each evaluated parameter point
for _, row in df.iterrows():
    m = row['mass_gev']
    tau = row['lifetime_mm']
    eff = row['efficiency']
    is_ex = row['excluded']
    
    if eff == df['efficiency'].max():
        txt_label = f"$\\mathbf{{\\epsilon = {eff:.2f}}}$\n(Peak)"
        ax.annotate(
            txt_label,
            xy=(m, tau),
            xytext=(11, 4),
            textcoords='offset points',
            fontsize=9.5,
            color='#0f172a',
            va='bottom',
            ha='left',
            zorder=6,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#f8fafc', edgecolor='#64748b', alpha=0.95, lw=0.8)
        )
    elif m >= 280:
        txt = f"$\\epsilon = {eff:.2f}$"
        ax.annotate(
            txt,
            xy=(m, tau),
            xytext=(-11, -2),
            textcoords='offset points',
            fontsize=9,
            color='#334155',
            va='center',
            ha='right',
            zorder=6
        )
    else:
        txt = f"$\\epsilon = {eff:.2f}$"
        ax.annotate(
            txt,
            xy=(m, tau),
            xytext=(10, -2),
            textcoords='offset points',
            fontsize=9,
            color='#334155',
            va='center',
            ha='left',
            zorder=6
        )

# 6. Set scale, limits, and tick locations
ax.set_yscale('log')
ax.set_xlim(100, 325)
ax.set_ylim(0.18, 90)

# Explicit mass ticks at scanned values
ax.set_xticks([120, 150, 180, 220, 260, 300])
ax.set_xticklabels(['120', '150', '180', '220', '260', '300'])

# Log ticks formatting for lifetime matching scanned decades
ax.set_yticks([0.3, 1.0, 3.0, 10.0, 30.0])
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{y:g}"))
ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=(0.2, 0.5, 2.0, 5.0, 50.0), numticks=10))
ax.yaxis.set_minor_formatter(ticker.NullFormatter())

# 7. Axes labels and title
ax.set_xlabel(r'Mass $m$ [GeV]', fontweight='bold', labelpad=8)
ax.set_ylabel(r'Proper Lifetime $c\tau$ [mm]', fontweight='bold', labelpad=8)
ax.set_title('Selection Efficiency in Irregular Mass–Lifetime Parameter Scan', pad=14, fontweight='bold', fontsize=12)

# Subtle scientific grid
ax.grid(True, which='major', linestyle='--', linewidth=0.7, color='#cbd5e1', alpha=0.75, zorder=1)
ax.grid(True, which='minor', linestyle=':', linewidth=0.5, color='#e2e8f0', alpha=0.5, zorder=1)

# 8. Colorbar for Selection Efficiency
cbar = fig.colorbar(sc_allowed, ax=ax, orientation='vertical', pad=0.03, shrink=0.92, aspect=20)
cbar.set_label(r'Selection Efficiency $\epsilon$', fontweight='bold', labelpad=10)
cbar.set_ticks(np.linspace(0.0, 0.20, 5))
cbar.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0, decimals=0))
cbar.ax.tick_params(labelsize=9.5)

# 9. Legend for theoretical exclusion status
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Theory allowed',
           markerfacecolor='#94a3b8', markeredgecolor='#1e293b', markeredgewidth=1.5, markersize=10),
    Line2D([0], [0], marker='s', color='w', label='Excluded by theory',
           markerfacecolor='#94a3b8', markeredgecolor='#dc2626', markeredgewidth=2.0, markersize=10),
]
legend = ax.legend(
    handles=legend_elements,
    loc='upper right',
    frameon=True,
    framealpha=0.95,
    edgecolor='#cbd5e1',
    facecolor='#ffffff',
    title='Theoretical Status',
    title_fontsize=9.5
)
legend.get_title().set_fontweight('bold')

# 10. Note clarifying discrete evaluated parameter points (placed in empty bottom-right region)
ax.text(
    0.97, 0.05,
    "Evaluated scan points only;\nintermediate values undefined.",
    transform=ax.transAxes,
    fontsize=8,
    style='italic',
    color='#64748b',
    va='bottom',
    ha='right',
    bbox=dict(boxstyle='square,pad=0.35', facecolor='#ffffff', edgecolor='#e2e8f0', alpha=0.9)
)

plt.tight_layout()
plt.savefig('plot.png', dpi=300)
plt.close()
