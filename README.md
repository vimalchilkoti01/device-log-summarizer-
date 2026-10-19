# Device Log Summarizer CLI

## Setup
```
pip install -r requirements.txt
```

## Run
```
python summarizer.py device_telemetry.csv     # Section 2: summary table + output/summary.json
python chart.py                               # Section 3: output/avg_temperature_chart.png
python -m unittest discover -s tests -v       # Section 1 & 2 tests
```
Options: `python summarizer.py data.csv --out output/summary.json --max-temp 80`

## Files
- `sanitize.py`: Section 1, `clean_readings()` drops None, non-numeric and negative values and caps readings at 500.0. Empty or all-invalid input returns `[]`.
- `summarizer.py`: Section 2, reads the CSV, groups by `device_id` (record count, mean temperature, ERROR count), removes devices with average temperature above 80.0, writes JSON and prints a table.
- `chart.py`: Section 3, a matplotlib bar chart of average temperature per device.
- `tests/`: unit tests.
- `output/`: sample output (`summary.json`, `sample_output.txt`, chart).
- `PROMPT_LOG.md`: how AI was used.

## Robustness
- A missing CSV or missing required columns prints a clear error and exits with code 1 (no traceback).
- Bad rows (non-numeric/empty temperature, empty device_id, unknown status) are skipped and counted.
- A sample `device_telemetry.csv` is included with deliberately bad rows. Replace it with the provided file if there is one.
