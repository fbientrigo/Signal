import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Ensure ordering matches domain sequence
channel_order = ["Barrel", "Transition", "Endcap", "Forward"]
df["channel"] = pd.Categorical(df["channel"], categories=channel_order, ordered=True)
df = df.sort_values("channel").reset_index(drop=True)

# Calculate asymmetric uncertainty intervals
# low and high are uncertainty bounds around estimate
y_err_lower = df["estimate"] - df["low"]
y_err_upper = df["high"] - df["estimate"]
yerr = np.vstack([y_err_lower, y_err_upper])

# Style setup for paper destination profile
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8.5,
    "axes.titlesize": 10.0,
    "axes.labelsize": 9.0,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "figure.dpi": 300,
    "savefig.dpi": 300,
})

fig, ax = plt.subplots(figsize=(3.6, 2.8))

# Color palette: unified primary color for categorical channels
primary_color = "#332288"
grid_color = "#E0E0E0"

# Plot error bars and point estimates
ax.errorbar(
    df["channel"],
    df["estimate"],
    yerr=yerr,
    fmt="o",
    color=primary_color,
    ecolor=primary_color,
    elinewidth=1.4,
    capsize=3.5,
    capthick=1.4,
    markersize=5.5,
    zorder=3,
)

# Subtle grid and spine styling
ax.set_axisbelow(True)
ax.yaxis.grid(True, linestyle="--", alpha=0.6, color=grid_color)
ax.xaxis.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#404040")
ax.spines["bottom"].set_color("#404040")

# Axis labels and title
ax.set_xlabel("Edited X", fontweight="medium", labelpad=6)
ax.set_ylabel("Edited Y", fontweight="medium", labelpad=6)
ax.set_title("Edited benchmark figure", fontweight="bold", pad=8)

# Set appropriate y-limits with headroom for error bars
ax.set_ylim(0.45, 0.85)
ax.set_yticks(np.arange(0.50, 0.85, 0.05))

# Annotate note regarding uncertainty bounds
ax.text(
    0.98,
    0.04,
    "Error bars indicate [low, high] bounds",
    transform=ax.transAxes,
    fontsize=7.0,
    color="#666666",
    ha="right",
    va="bottom",
    style="italic",
)

plt.tight_layout()
plt.savefig("edited_plot.png", dpi=300)
plt.close()
