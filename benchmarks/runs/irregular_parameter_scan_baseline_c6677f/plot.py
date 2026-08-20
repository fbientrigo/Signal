import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'data.csv')
output_path = os.path.join(script_dir, 'plot.png')

df = pd.read_csv(csv_path)

df['mass_gev'] = df['mass_gev'].astype(float)
df['lifetime_mm'] = df['lifetime_mm'].astype(float)
df['efficiency'] = df['efficiency'].astype(float)
df['excluded'] = df['excluded'].astype(bool)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10.5,
    'ytick.labelsize': 10.5,
    'legend.fontsize': 10,
    'figure.titlesize': 14
})

fig, ax = plt.subplots(figsize=(8.5, 6), dpi=300)

cmap = plt.cm.viridis
vmin = 0.0
vmax = 0.20
norm = plt.Normalize(vmin=vmin, vmax=vmax)

allowed = df[~df['excluded']]
excluded = df[df['excluded']]

sc_allowed = ax.scatter(
    allowed['mass_gev'],
    allowed['lifetime_mm'],
    c=allowed['efficiency'],
    cmap=cmap,
    norm=norm,
    s=180,
    marker='o',
    edgecolors='black',
    linewidths=1.5,
    zorder=4,
    label='Allowed by theory'
)

sc_excluded = ax.scatter(
    excluded['mass_gev'],
    excluded['lifetime_mm'],
    c=excluded['efficiency'],
    cmap=cmap,
    norm=norm,
    s=190,
    marker='s',
    edgecolors='#D9534F',
    linewidths=2.0,
    hatch='///',
    zorder=4,
    label='Excluded by theory'
)

ax.scatter(
    excluded['mass_gev'],
    excluded['lifetime_mm'],
    color='#D9534F',
    s=65,
    marker='x',
    linewidths=2.0,
    zorder=5
)

for _, row in df.iterrows():
    eff_val = row['efficiency']
    x_pos = row['mass_gev']
    y_pos = row['lifetime_mm']
    
    if eff_val == df['efficiency'].max():
        ax.annotate(
            f'Max Efficiency\n$\\varepsilon = {eff_val:.2f}$ ({int(eff_val*100)}%)',
            xy=(x_pos, y_pos),
            xytext=(x_pos + 14, y_pos * 1.7),
            arrowprops=dict(
                arrowstyle='->',
                lw=1.5,
                color='#1b5e20',
                shrinkB=7,
                shrinkA=0
            ),
            fontweight='bold',
            fontsize=10,
            color='#1b5e20',
            bbox=dict(
                boxstyle='round,pad=0.35',
                facecolor='#e8f5e9',
                edgecolor='#2e7d32',
                lw=1.2
            ),
            zorder=6
        )
    else:
        ax.text(
            x_pos,
            y_pos * 1.30,
            f'{eff_val:.2f}',
            fontsize=9,
            ha='center',
            va='bottom',
            color='#222222',
            fontweight='semibold',
            bbox=dict(
                boxstyle='round,pad=0.15',
                facecolor='white',
                alpha=0.88,
                edgecolor='#cccccc',
                lw=0.6
            ),
            zorder=6
        )

ax.set_yscale('log')
ax.set_xlabel(r'Mass $m$ [$\mathrm{GeV}$]', fontweight='bold')
ax.set_ylabel(r'Lifetime $c\tau$ [$\mathrm{mm}$]', fontweight='bold')
ax.set_title('Selection Efficiency in Irregular Mass–Lifetime Parameter Scan', fontweight='bold', pad=12)

ax.set_xlim(100, 320)
ax.set_ylim(0.15, 100)

ax.set_xticks([120, 150, 180, 220, 260, 300])
ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())

ax.set_yticks([0.3, 1.0, 3.0, 10.0, 30.0, 50.0])
ax.get_yaxis().set_major_formatter(ticker.ScalarFormatter())

ax.grid(True, which='major', linestyle='--', alpha=0.45, color='gray')
ax.grid(True, which='minor', linestyle=':', alpha=0.25, color='gray')
ax.set_axisbelow(True)

cbar = fig.colorbar(sc_allowed, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label(r'Selection Efficiency $\varepsilon$', fontweight='bold')
cbar.set_ticks(np.linspace(0.0, 0.20, 5))
cbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

legend = ax.legend(
    loc='upper right',
    frameon=True,
    fancybox=True,
    framealpha=0.92,
    borderpad=0.8
)
legend.get_frame().set_edgecolor('#cccccc')

plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print("plot.png generated successfully.")
