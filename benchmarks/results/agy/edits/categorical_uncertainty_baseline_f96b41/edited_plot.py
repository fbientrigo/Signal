import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set publication-quality visual style
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'axes.edgecolor': '#333333',
    'axes.linewidth': 1.2,
    'grid.color': '#e0e0e0',
    'grid.linestyle': '--',
    'grid.linewidth': 0.8,
    'grid.alpha': 0.7,
})

# Load the dataset
data_path = 'data.csv'
df = pd.read_csv(data_path)

# Compute asymmetric error components for matplotlib errorbar: [lower_errors, upper_errors]
y_err_low = df['estimate'] - df['low']
y_err_high = df['high'] - df['estimate']
y_err = [y_err_low.values, y_err_high.values]

# Color palette for detector channels
colors = ['#332288', '#88CCEE', '#44AA99', '#117733']

fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

# Add subtle background horizontal grid
ax.grid(True, axis='y', zorder=0)
ax.set_axisbelow(True)

x_positions = np.arange(len(df))

# Plot each channel with asymmetric uncertainty bounds
for i, row in df.iterrows():
    # Error bar
    ax.errorbar(
        x=x_positions[i],
        y=row['estimate'],
        yerr=[[y_err_low[i]], [y_err_high[i]]],
        fmt='o',
        markersize=9,
        markerfacecolor=colors[i],
        markeredgecolor='#222222',
        markeredgewidth=1.2,
        color=colors[i],
        ecolor='#333333',
        elinewidth=2.0,
        capsize=6,
        capthick=1.8,
        zorder=3,
        label=f"{row['channel']}"
    )
    
    # Numeric annotation positioned to the right of each point
    annotation_text = f"{row['estimate']:.2f}\n[{row['low']:.2f}, {row['high']:.2f}]"
    ax.annotate(
        annotation_text,
        xy=(x_positions[i], row['estimate']),
        xytext=(12, 0),
        textcoords='offset points',
        va='center',
        ha='left',
        fontsize=9.5,
        fontweight='medium',
        color='#222222',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#d0d0d0', alpha=0.85, linewidth=0.8),
        zorder=4
    )

# Formatting axes
ax.set_xticks(x_positions)
ax.set_xticklabels(df['channel'], fontsize=11, fontweight='semibold')
ax.set_xlabel('Edited X', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('Edited Y', fontsize=12, fontweight='bold', labelpad=10)

# Set Y-axis limits with padding for clean presentation
y_min = df['low'].min() - 0.06
y_max = df['high'].max() + 0.08
ax.set_ylim(y_min, y_max)
ax.set_xlim(-0.6, len(df) - 0.2)

# Title and subtitle
ax.set_title('Edited benchmark figure', fontsize=14, fontweight='bold', pad=10)

# Add informative note regarding bounds
note_text = (
    "Note: Points indicate central estimates. Error bars represent\n"
    "the reported [low, high] uncertainty bounds per channel."
)
ax.text(
    0.03, 0.05, note_text,
    transform=ax.transAxes,
    fontsize=8.5,
    style='italic',
    color='#444444',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor='#cccccc', alpha=0.9, linewidth=0.8)
)

plt.tight_layout()
plt.savefig('edited_plot.png', dpi=300, bbox_inches='tight')
print("Plot successfully saved to plot.png")
