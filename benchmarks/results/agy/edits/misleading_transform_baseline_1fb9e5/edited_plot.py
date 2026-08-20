import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import ConnectionPatch
from matplotlib.ticker import FuncFormatter

def main():
    # Read the dataset
    df = pd.read_csv('data.csv')

    # Separate zero dose (baseline / control) and non-zero doses
    df_zero = df[df['dose_gy'] == 0.0]
    df_pos = df[df['dose_gy'] > 0.0]

    # Create figure with broken x-axis to accommodate zero-dose baseline on a log-dose scale
    fig, (ax_zero, ax_log) = plt.subplots(
        1, 2,
        figsize=(8.5, 5.2),
        dpi=300,
        gridspec_kw={'width_ratios': [1, 6], 'wspace': 0.05},
        sharey=True
    )

    # Plot color palette & styling
    primary_color = '#332288'
    edge_color = '#88CCEE'
    zero_line_color = '#44AA99'

    # --- 1. Left Panel: Zero-Dose Baseline ---
    ax_zero.plot(
        df_zero['dose_gy'],
        df_zero['response_mv'],
        marker='o',
        markersize=7.5,
        color=primary_color,
        markeredgecolor=edge_color,
        markeredgewidth=1.2,
        zorder=5,
        label='Baseline (0 Gy)'
    )
    ax_zero.axhline(0, color=zero_line_color, linestyle=':', linewidth=1.0, alpha=0.7, zorder=2)
    ax_zero.set_xlim(-0.05, 0.05)
    ax_zero.set_xticks([0.0])
    ax_zero.set_xticklabels(['0'])
    ax_zero.set_ylabel('Edited Y', fontsize=12, fontweight='bold', color='#1a1a1a')
    
    # Hide unwanted spines on left panel
    ax_zero.spines['top'].set_visible(False)
    ax_zero.spines['right'].set_visible(False)
    ax_zero.spines['left'].set_color('#333333')
    ax_zero.spines['bottom'].set_color('#333333')
    ax_zero.grid(True, which='both', axis='y', linestyle='--', alpha=0.4, color='#c0c0c0')

    # --- 2. Right Panel: Positive Doses (Logarithmic Scale) ---
    line_pos, = ax_log.plot(
        df_pos['dose_gy'],
        df_pos['response_mv'],
        marker='o',
        markersize=7.5,
        color=primary_color,
        markeredgecolor=edge_color,
        markeredgewidth=1.2,
        linewidth=1.8,
        zorder=5,
        label='Sensor response'
    )
    ax_log.axhline(0, color=zero_line_color, linestyle=':', linewidth=1.0, alpha=0.7, zorder=2, label='Zero response (0 mV)')
    
    ax_log.set_xscale('log')
    ax_log.set_xlim(0.06, 160)
    pos_ticks = [0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]
    ax_log.set_xticks(pos_ticks)
    ax_log.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f'{val:g}'))
    
    # Configure grids and spines on right panel
    ax_log.grid(True, which='major', axis='both', linestyle='--', alpha=0.4, color='#c0c0c0')
    ax_log.grid(True, which='minor', axis='x', linestyle=':', alpha=0.2, color='#c0c0c0')
    ax_log.spines['top'].set_visible(False)
    ax_log.spines['left'].set_visible(False)
    ax_log.spines['right'].set_visible(False)
    ax_log.spines['bottom'].set_color('#333333')
    ax_log.tick_params(left=False, labelleft=False)

    # Set shared Y limits
    ax_zero.set_ylim(-1.5, 20.0)

    # --- 3. Connect Baseline to Log Curve Across Break ---
    y_zero_val = df_zero['response_mv'].values[0]
    x_first_pos = df_pos['dose_gy'].values[0]
    y_first_pos = df_pos['response_mv'].values[0]

    con = ConnectionPatch(
        xyA=(0.0, y_zero_val),
        coordsA=ax_zero.transData,
        xyB=(x_first_pos, y_first_pos),
        coordsB=ax_log.transData,
        linestyle='--',
        color=primary_color,
        linewidth=1.5,
        alpha=0.75,
        zorder=4
    )
    fig.add_artist(con)

    # --- 4. Draw Axis Break Slashes on Bottom Spines ---
    d_x = 0.012
    d_y = 0.022
    slash_kw = dict(color='#333333', clip_on=False, linewidth=1.3)

    # Right end of ax_zero bottom spine
    ax_zero.plot((1 - d_x, 1 + d_x), (-d_y, +d_y), transform=ax_zero.transAxes, **slash_kw)
    # Left end of ax_log bottom spine
    ax_log.plot((-d_x, +d_x), (-d_y, +d_y), transform=ax_log.transAxes, **slash_kw)

    # --- 5. Labels, Title, and Annotations ---
    fig.text(0.53, 0.04, 'Edited X', ha='center', fontsize=12, fontweight='bold', color='#1a1a1a')
    fig.suptitle('Edited benchmark figure', fontsize=14, fontweight='bold', color='#1a1a1a', y=0.96)

    # Add descriptive annotation for baseline response
    ax_zero.annotate(
        f'Baseline:\n{y_zero_val:.2f} mV',
        xy=(0.0, y_zero_val),
        xytext=(0.0, 2.5),
        arrowprops=dict(arrowstyle='->', color='#333333', lw=1.0),
        fontsize=9,
        ha='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#cccccc', alpha=0.9)
    )

    # Legend
    handles, labels = ax_log.get_legend_handles_labels()
    # Add custom handle for dashed baseline transition
    from matplotlib.lines import Line2D
    baseline_line = Line2D([0], [0], color=primary_color, linestyle='--', linewidth=1.5, label='Baseline transition')
    ax_log.legend(
        handles=[handles[0], baseline_line, handles[1]],
        loc='upper left',
        frameon=True,
        framealpha=0.95,
        facecolor='#ffffff',
        edgecolor='#cccccc',
        fontsize=10
    )

    plt.subplots_adjust(bottom=0.15, top=0.88, left=0.12, right=0.95)
    plt.savefig('edited_plot.png', dpi=300)
    print("Successfully generated plot.png")

if __name__ == '__main__':
    main()
