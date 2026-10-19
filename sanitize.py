"""Section 1: clean and normalize sensor readings."""

MAX_READING = 500.0


def clean_readings(values):
    """Return a list of floats: drop None, non-numeric and negative values,
    and cap anything above 500.0. Never raises for bad input."""
    if not values:
        return []

    cleaned = []
    for value in values:
        if value is None or isinstance(value, bool):
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if number != number or number < 0:  # NaN or negative error flag
            continue
        cleaned.append(min(number, MAX_READING))
    return cleaned
