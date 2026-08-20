from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Load data
data_path = Path(__file__).parent / "data.csv"
df = pd.read_csv(data_path)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Figure setup
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

# Plot line and points
ax.plot(
    df["date"],
    df["temperature_c"],
    marker="o",
    markersize=5,
    linestyle="-",
    linewidth=1.8,
    color="#1f77b4",
    label="Daily temperature",
)

# Reference line at freezing threshold 0 °C
ax.axhline(0, color="#888888", linestyle="--", linewidth=1, alpha=0.7, label="Freezing point (0 °C)")

# Formatting
ax.set_title("Daily Temperature (January 2026)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Date", fontsize=11, labelpad=8)
ax.set_ylabel("Temperature (°C)", fontsize=11, labelpad=8)

# Format x-axis dates
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

# Grid and styling
ax.grid(True, which="major", linestyle=":", alpha=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=True, loc="upper right")

# Set sensible y-limits with padding
ymin = min(df["temperature_c"]) - 1
ymax = max(df["temperature_c"]) + 1
ax.set_ylim(ymin, ymax)

plt.tight_layout()

# Save plot
output_path = Path(__file__).parent / "plot.png"
plt.savefig(output_path, dpi=300)
plt.close(fig)
print("Plot successfully saved to plot.png")
