"""Basic statistical functions for ACF analysis."""

from __future__ import annotations

import math
from typing import Sequence


def mean(values: Sequence[float]) -> float:
    """Arithmetic mean."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def std_dev(values: Sequence[float]) -> float:
    """Population standard deviation."""
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def pearson_correlation(x: Sequence[float], y: Sequence[float]) -> float:
    """Pearson correlation coefficient between two sequences.

    Returns r in [-1, 1]. Returns 0.0 if insufficient data.
    """
    n = min(len(x), len(y))
    if n < 2:
        return 0.0

    x = list(x[:n])
    y = list(y[:n])

    mx = mean(x)
    my = mean(y)

    numerator = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    denom_x = math.sqrt(sum((xi - mx) ** 2 for xi in x))
    denom_y = math.sqrt(sum((yi - my) ** 2 for yi in y))

    if denom_x == 0 or denom_y == 0:
        return 0.0

    return numerator / (denom_x * denom_y)


def percentile(values: Sequence[float], p: float) -> float:
    """Calculate p-th percentile (0-100)."""
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * (p / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] * (c - k) + sorted_vals[c] * (k - f)
