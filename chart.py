"""Section 3: bar chart of average temperature per device (from summary.json)."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # works without a display
import matplotlib.pyplot as plt


def main(json_path="output/summary.json", out_path="output/avg_temperature_chart.png"):
    path = Path(json_path)
    if not path.is_file():
        print(f"Error: {path} not found. Run summarizer.py first.", file=sys.stderr)
        return 1
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        print("Error: summary is empty, nothing to plot.", file=sys.stderr)
        return 1

    devices = [d["device_id"] for d in data]
    temps = [d["avg_temperature"] for d in data]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(devices, temps, color="#2a7ab9")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature")
    ax.set_ylim(0, max(temps) * 1.15)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    print(f"Chart saved: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
