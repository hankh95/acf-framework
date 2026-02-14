"""Metric type definitions for hypothesis testing and data collection."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class MetricType(Enum):
    """Types of hypothesis metrics."""
    LATENCY = "latency"
    ACCURACY = "accuracy"
    THROUGHPUT = "throughput"
    COUNT = "count"
    RATIO = "ratio"
    BOOLEAN = "boolean"
    SCORE = "score"
    DISTRIBUTION = "distribution"


class ComparisonOp(Enum):
    """Comparison operators for pass/fail determination."""
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    EQ = "=="


@dataclass
class HypothesisMetric:
    """A single hypothesis metric measurement."""

    hypothesis_id: str
    metric_name: str
    metric_type: MetricType
    target: float
    comparison: ComparisonOp
    actual: float
    passed: bool
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "metric_name": self.metric_name,
            "metric_type": self.metric_type.value,
            "target": self.target,
            "comparison": self.comparison.value,
            "actual": self.actual,
            "passed": self.passed,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> HypothesisMetric:
        return cls(
            hypothesis_id=data["hypothesis_id"],
            metric_name=data["metric_name"],
            metric_type=MetricType(data["metric_type"]),
            target=data["target"],
            comparison=ComparisonOp(data["comparison"]),
            actual=data["actual"],
            passed=data["passed"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
        )

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return (
            f"{self.hypothesis_id} [{status}]: {self.metric_name} = {self.actual:.4f} "
            f"(target: {self.comparison.value} {self.target})"
        )
