import matplotlib.pyplot as plt
import pandas as pd

# Set style for publication-ready scientific figure
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'mathtext.fontset': 'dejavusans',
    'axes.linewidth': 1.0,
    'grid.linewidth': 0.6,
    'lines.linewidth': 2.0,
    'lines.markersize': 6,
})

# Load data
df = pd.read_csv('data.csv')

# Calculate asymmetric error bar spans
yerr_low = df['mean_height_cm'] - df['ci_low']
yerr_high = df['ci_high'] - df['mean_height_cm']
yerr = [yerr_low, yerr_high]

fig, ax = plt.subplots(figsize=(6.5, 4.8), dpi=300)

# Colors
primary_color = '#1b5e20'  # Deep botanical green
fill_color = '#4caf50'     # Softer green for confidence band

# Plot confidence interval shaded region
ax.fill_between(
    df['week'],
    df['ci_low'],
    df['ci_high'],
    color=fill_color,
    alpha=0.25,
    label='Confidence Interval'
)

# Plot line and points with error bars
ax.errorbar(
    df['week'],
    df['mean_height_cm'],
    yerr=yerr,
    fmt='-o',
    color=primary_color,
    ecolor=primary_color,
    elinewidth=1.5,
    capsize=4,
    capthick=1.2,
    markerfacecolor='white',
    markeredgecolor=primary_color,
    markeredgewidth=1.8,
    label='Mean Height',
    zorder=3
)

# Formatting axes and labels
ax.set_xlabel('Time (weeks)', fontweight='bold', labelpad=8)
ax.set_ylabel('Plant Height (cm)', fontweight='bold', labelpad=8)
ax.set_title('Plant Growth Trajectory Over Time', fontweight='bold', pad=12)

# Set ticks and limits
ax.set_xticks(df['week'])
ax.set_xlim(-0.3, 8.3)
ax.set_ylim(0, 25)

# Styling grid and spines
ax.grid(True, linestyle='--', alpha=0.5, color='gray', zorder=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#333333')
ax.spines['bottom'].set_color('#333333')

# Legend
ax.legend(frameon=True, facecolor='white', edgecolor='#cccccc', framealpha=0.9, loc='upper left')

plt.tight_layout()
plt.savefig('plot.png', dpi=300)
plt.close()
