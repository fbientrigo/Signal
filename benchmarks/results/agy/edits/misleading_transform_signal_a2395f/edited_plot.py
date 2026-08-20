import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data
df = pd.read_csv("data.csv")
dose = df["dose_gy"].values
response = df["response_mv"].values

# Configure publication-quality style
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 9,
    "axes.labelsize": 9.5,
    "axes.titlesize": 10.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "lines.linewidth": 1.5,
    "lines.markersize": 5.5,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#334155",
    "text.color": "#1e293b",
    "axes.labelcolor": "#1e293b",
    "xtick.color": "#334155",
    "ytick.color": "#334155",
    "figure.facecolor": "#ffffff",
    "axes.facecolor": "#ffffff",
    "savefig.facecolor": "#ffffff",
})

# Create figure
fig, ax = plt.subplots(figsize=(5.2, 3.8), dpi=300)

# Colors
primary_color = "#332288"
fit_color = "#88CCEE"
ref_color = "#44AA99"
highlight_color = "#117733"

# Linear fit across full range to show constant sensitivity (linear physical response)
slope, intercept = np.polyfit(dose, response, 1)
fit_x = np.linspace(0, 105, 200)
fit_y = slope * fit_x + intercept

# Plot reference line at y = 0
ax.axhline(0, color=ref_color, linestyle="--", linewidth=0.8, zorder=1, label="Zero response baseline (0 mV)")

# Plot linear fit line
ax.plot(fit_x, fit_y, color=fit_color, linestyle="-", linewidth=1.4, alpha=0.85, zorder=2,
        label=f"Linear fit (sensitivity: {slope:.3f} mV/Gy)")

# Plot measured points
ax.scatter(dose, response, color=primary_color, edgecolor="white", linewidth=0.7, s=36, zorder=3,
           label="Measured response")

# Main axes limits and formatting
ax.set_xlim(-3, 105)
ax.set_ylim(-1.5, 20)
ax.set_xlabel("Edited X", fontweight="medium")
ax.set_ylabel("Edited Y", fontweight="medium")
ax.set_title("Edited benchmark figure", fontweight="bold", pad=8)

# Gridlines
ax.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1", zorder=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend (placed in lower right)
ax.legend(loc="lower right", frameon=True, facecolor="#f8fafc", edgecolor="#e2e8f0", fontsize=7.5)

# Inset zoom to resolve low-dose regime (0 to 3 Gy) without misleading log distortion
axins = ax.inset_axes([0.12, 0.48, 0.44, 0.44])

# Plot data on inset
fit_x_inset = np.linspace(-0.1, 3.2, 100)
fit_y_inset = slope * fit_x_inset + intercept

axins.axhline(0, color=ref_color, linestyle="--", linewidth=0.8, zorder=1)
axins.plot(fit_x_inset, fit_y_inset, color=fit_color, linestyle="-", linewidth=1.3, alpha=0.85, zorder=2)

low_mask = dose <= 3.0
axins.scatter(dose[low_mask], response[low_mask], color=primary_color, edgecolor="white", linewidth=0.7, s=32, zorder=3)

# Highlight baseline measurement at dose = 0 Gy
axins.scatter([0.0], [-0.20], color=highlight_color, edgecolor="white", linewidth=0.8, s=40, zorder=4)
axins.annotate("0 Gy: −0.20 mV", xy=(0.0, -0.20), xytext=(0.3, -0.32),
               fontsize=7.0, color="#117733", fontweight="semibold",
               arrowprops=dict(arrowstyle="->", color="#117733", lw=0.7, shrinkA=3, shrinkB=3))

# Inset limits and styling
axins.set_xlim(-0.2, 3.3)
axins.set_ylim(-0.45, 0.55)
axins.set_title("Edited benchmark figure", fontsize=7.5, fontweight="bold", pad=4, color="#1e293b")
axins.set_xlabel("Edited X", fontsize=7.0, labelpad=2)
axins.set_ylabel("Edited Y", fontsize=7.0, labelpad=2)
axins.tick_params(axis="both", labelsize=6.5, pad=2)
axins.grid(True, linestyle=":", alpha=0.4, color="#cbd5e1", zorder=0)
axins.spines["top"].set_visible(False)
axins.spines["right"].set_visible(False)
axins.set_facecolor("#fafbfc")

# Zoom indicator lines connecting main axes to inset
ax.indicate_inset_zoom(axins, edgecolor="#64748b", alpha=0.6, linewidth=0.8)

# Tight layout and save
plt.tight_layout()
plt.savefig("edited_plot.png", dpi=300, bbox_inches="tight")
plt.close()
print("plot.png generated successfully.")
