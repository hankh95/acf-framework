"""Statistical analysis for hypothesis testing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from acf.utils.stats import pearson_correlation


@dataclass
class HypothesisResult:
    """Result of evaluating a hypothesis against collected data."""

    hypothesis_id: str
    status: str  # "supported", "partially_supported", "not_supported", "insufficient_data"
    evidence: str
    value: float = 0.0
    target: float = 0.0
    confidence: str = ""


def evaluate_correlation(
    hypothesis_id: str,
    x_values: list[float],
    y_values: list[float],
    target_r: float,
    direction: str = "less_than",
) -> HypothesisResult:
    """Evaluate a correlation hypothesis (e.g., r < 0.3)."""
    if len(x_values) < 3 or len(y_values) < 3:
        return HypothesisResult(
            hypothesis_id=hypothesis_id,
            status="insufficient_data",
            evidence=f"Need at least 3 data points, got {min(len(x_values), len(y_values))}",
        )

    r = pearson_correlation(x_values, y_values)

    if direction == "less_than":
        passed = abs(r) < target_r
    else:
        passed = abs(r) > target_r

    return HypothesisResult(
        hypothesis_id=hypothesis_id,
        status="supported" if passed else "not_supported",
        evidence=f"r = {r:.3f} (target: {direction} {target_r})",
        value=r,
        target=target_r,
    )


def evaluate_threshold(
    hypothesis_id: str,
    value: float,
    target: float,
    comparison: str = "GE",
    description: str = "",
) -> HypothesisResult:
    """Evaluate a threshold hypothesis (e.g., score >= 95%)."""
    ops = {
        "GE": value >= target,
        "GT": value > target,
        "LE": value <= target,
        "LT": value < target,
        "EQ": value == target,
    }
    passed = ops.get(comparison, False)

    return HypothesisResult(
        hypothesis_id=hypothesis_id,
        status="supported" if passed else "not_supported",
        evidence=f"{description}: {value:.3f} {comparison} {target}",
        value=value,
        target=target,
    )
