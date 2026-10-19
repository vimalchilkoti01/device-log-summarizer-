"""Section 2: Device Log Summarizer CLI.

Usage: python summarizer.py [csv_path] [--out output/summary.json] [--max-temp 80]
"""
import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED_COLUMNS = {"device_id", "status", "temperature"}
VALID_STATUSES = {"ACTIVE", "WARNING", "ERROR"}


def read_telemetry(csv_path):
    """Read rows from the CSV. Returns (rows, skipped_count)."""
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")

    rows, skipped = [], 0
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = {h.strip() for h in (reader.fieldnames or [])}
        missing = REQUIRED_COLUMNS - header
        if missing:
            raise ValueError(f"CSV is missing columns: {', '.join(sorted(missing))}")

        for raw in reader:
            row = {k.strip(): (v or "").strip() for k, v in raw.items() if k}
            device_id = row.get("device_id", "")
            status = row.get("status", "").upper()
            try:
                temperature = float(row.get("temperature", ""))
            except ValueError:
                skipped += 1
                continue
            if not device_id or status not in VALID_STATUSES or temperature != temperature:
                skipped += 1
                continue
            rows.append({"device_id": device_id, "status": status, "temperature": temperature})
    return rows, skipped


def aggregate(rows):
    """Group by device_id: record count, mean temperature, ERROR count."""
    groups = defaultdict(lambda: {"total_records": 0, "temp_sum": 0.0, "error_count": 0})
    for row in rows:
        g = groups[row["device_id"]]
        g["total_records"] += 1
        g["temp_sum"] += row["temperature"]
        if row["status"] == "ERROR":
            g["error_count"] += 1

    return [
        {
            "device_id": device_id,
            "total_records": g["total_records"],
            "avg_temperature": round(g["temp_sum"] / g["total_records"], 2),
            "error_count": g["error_count"],
        }
        for device_id, g in sorted(groups.items())
    ]


def filter_devices(summary, max_avg_temp=80.0):
    """Drop devices whose average temperature is above the limit."""
    return [d for d in summary if d["avg_temperature"] <= max_avg_temp]


def export_json(summary, out_path):
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def print_table(summary):
    header = f"{'Device':<10}{'Records':>9}{'Avg Temp':>11}{'Errors':>8}"
    print(header)
    print("-" * len(header))
    for d in summary:
        print(f"{d['device_id']:<10}{d['total_records']:>9}{d['avg_temperature']:>11.2f}{d['error_count']:>8}")
    if not summary:
        print("(no devices to show)")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarize device telemetry CSV logs.")
    parser.add_argument("csv_path", nargs="?", default="device_telemetry.csv")
    parser.add_argument("--out", default="output/summary.json")
    parser.add_argument("--max-temp", type=float, default=80.0)
    args = parser.parse_args(argv)

    try:
        rows, skipped = read_telemetry(args.csv_path)
    except (FileNotFoundError, ValueError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    summary = filter_devices(aggregate(rows), args.max_temp)
    export_json(summary, args.out)
    print_table(summary)
    print(f"\nValid rows: {len(rows)} | Skipped bad rows: {skipped} | Saved: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
