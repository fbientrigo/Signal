from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def main():
    data_path = Path(__file__).parent / "data.csv"
    output_path = Path(__file__).parent / "plot.png"

    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])

    # Plot setup
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    # Reference line at 0 °C (Freezing point)
    ax.axhline(0, color="#88CCEE", linestyle="--", linewidth=1.0, alpha=0.7, label="Freezing Point (0 °C)")

    # Plot temperature line and points
    ax.plot(
        df["date"],
        df["temperature_c"],
        marker="o",
        color="#332288",
        linewidth=2,
        markersize=6,
        label="Daily Temperature (°C)",
    )

    # Formatting
    ax.set_title("Edited benchmark figure", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Edited X", fontsize=11, labelpad=8)
    ax.set_ylabel("Edited Y", fontsize=11, labelpad=8)

    # Date formatting on X-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    fig.autofmt_xdate(rotation=45, ha="right")

    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(frameon=True, loc="upper right")

    # Tight layout and save
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print("Plot generated successfully.")


if __name__ == "__main__":
    main()
