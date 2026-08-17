"""
Statistics tool.

Computes descriptive statistics for a list of numbers.

The AI agent routes requests such as
"what is the average of 1 2 3 4 5" to this tool.

Supported statistics:
- Count and sum
- Mean (arithmetic average)
- Median
- Mode
- Min, max and range
- Population and sample variance
- Population and sample standard deviation
- Quartiles and interquartile range (IQR)
- Sum of squares
"""


import math
import re
from collections import Counter


def _parse_numbers(text: str) -> list[float]:
    """
    Extract every number from the input text.
    """

    matches = re.findall(
        r"-?\d+(?:\.\d+)?",
        text
    )

    return [float(value) for value in matches]


def _fmt(value: float | int | None):
    """
    Format a number for clean display.
    """

    if value is None:
        return None

    if isinstance(value, float) and value.is_integer():
        return int(value)

    return round(value, 6)


def statistics(text: str) -> dict:
    """
    Compute descriptive statistics for numbers
    found in the input.

    Args:
        text (str):
            Text containing numbers.

            Example:
            "1, 2, 3, 4, 5"

    Returns:
        dict:
            Statistics or error.
    """

    numbers = _parse_numbers(text)

    if not numbers:

        return {
            "tool": "statistics",
            "error": "No numbers found in input"
        }

    count = len(numbers)

    total = sum(numbers)

    mean = total / count

    sorted_numbers = sorted(numbers)

    # Median.
    middle = count // 2

    if count % 2 == 1:

        median = sorted_numbers[middle]

    else:

        median = (
            sorted_numbers[middle - 1]
            + sorted_numbers[middle]
        ) / 2

    # Quartiles.
    lower_half = sorted_numbers[:middle]

    if count % 2 == 1:
        upper_half = sorted_numbers[middle + 1:]
    else:
        upper_half = sorted_numbers[middle:]

    def _median(values):
        if not values:
            return None
        length = len(values)
        mid = length // 2
        if length % 2 == 1:
            return values[mid]
        return (values[mid - 1] + values[mid]) / 2

    q1 = _median(lower_half)

    q3 = _median(upper_half)

    # Mode.
    counts = Counter(numbers)

    max_count = max(counts.values())

    modes = sorted(
        value for value, frequency in counts.items()
        if frequency == max_count
    )

    # Variance.
    variance_sample = (
        sum((value - mean) ** 2 for value in numbers)
        / (count - 1)
        if count > 1 else 0.0
    )

    variance_population = (
        sum((value - mean) ** 2 for value in numbers)
        / count
    )

    stddev_sample = math.sqrt(variance_sample)

    stddev_population = math.sqrt(variance_population)

    iqr = (
        (q3 - q1)
        if q1 is not None and q3 is not None else None
    )

    return {
        "tool": "statistics",
        "count": count,
        "sum": _fmt(total),
        "mean": _fmt(mean),
        "median": _fmt(median),
        "mode": modes,
        "min": _fmt(min(numbers)),
        "max": _fmt(max(numbers)),
        "range": _fmt(max(numbers) - min(numbers)),
        "variance_population": _fmt(variance_population),
        "variance_sample": _fmt(variance_sample),
        "stddev_population": _fmt(stddev_population),
        "stddev_sample": _fmt(stddev_sample),
        "q1": _fmt(q1) if q1 is not None else None,
        "q3": _fmt(q3) if q3 is not None else None,
        "iqr": _fmt(iqr) if iqr is not None else None,
    }
