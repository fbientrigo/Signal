import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Load data
data_path = Path(__file__).parent / 'data.csv'
df = pd.read_csv(data_path)

# Publication styling (Signal paper profile)
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 8.5,
    'axes.labelsize': 8.5,
    'axes.titlesize': 9.5,
    'xtick.labelsize': 7.5,
    'ytick.labelsize': 7.5,
    'legend.fontsize': 7.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.edgecolor': '#252525',
    'axes.linewidth': 0.8,
    'xtick.color': '#252525',
    'ytick.color': '#252525',
    'text.color': '#252525',
})

# Create figure
fig, ax = plt.subplots(figsize=(3.4, 2.5))

# Colors
primary_color = '#332288'
band_color = '#332288'

# Plot confidence interval band
ax.fill_between(
    df['week'],
    df['ci_low'],
    df['ci_high'],
    color=band_color,
    alpha=0.2,
    linewidth=0,
    label='Confidence interval',
)

# Plot mean trajectory with points
ax.plot(
    df['week'],
    df['mean_height_cm'],
    color=primary_color,
    linewidth=1.35,
    marker='o',
    markersize=4.5,
    markerfacecolor=primary_color,
    markeredgecolor='none',
    label='Mean height',
)

# Configure axes
ax.set_title('Edited benchmark figure')
ax.set_xlabel('Edited X')
ax.set_ylabel('Edited Y')
ax.set_xticks(df['week'])
ax.set_xlim(-0.3, 8.3)
ax.set_ylim(0, 25)

# Add subtle horizontal grid for legibility in print
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color='#D9D7D0', alpha=0.7)
ax.set_axisbelow(True)

# Legend
ax.legend(frameon=False, loc='upper left')

# Layout and save
fig.tight_layout()
output_path = Path(__file__).parent / 'plot.png'
output_path = Path(__file__).parent / 'edited_plot.png'
fig.savefig(output_path, dpi=300)
plt.close(fig)
