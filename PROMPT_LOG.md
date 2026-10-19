# PROMPT_LOG

This log covers the AI prompting for Section 3 (charting).

## 1. Initial prompt

> Write a Python script that loads `output/summary.json` (a list of objects with `device_id`, `total_records`, `avg_temperature`, `error_count`) and generates a bar chart comparing the average temperature per device using matplotlib. Save it as a PNG.

## 2. Mistakes in the AI's first attempt

The first version ran, but the chart had problems when I reviewed it:
- **No title and no axis labels**: you couldn't tell what the bars or the y-axis meant.
- No value labels on the bars, so exact averages had to be guessed.
- It would crash with a traceback if `summary.json` was missing, and it opened the file without closing it.
- With longer device IDs, the x-axis labels would overlap.

## 3. Follow-up prompt

> The chart has no title or axis labels. Add the title "Average Temperature per Device", label the x-axis "Device ID" and the y-axis "Average Temperature", show each bar's value on top, rotate the x-labels so long IDs don't overlap, and use tight_layout. Also handle a missing or empty JSON file with a clear error message instead of a traceback, and use a non-GUI backend so it runs on a server.

## 4. What I checked myself

I ran the fixed script against my Section 2 output and confirmed the bar values match `summary.json`.
