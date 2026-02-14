"""Python dataclasses for the 3 ACF data record types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class CommonEnvelope:
    """Common fields for all ACF data records."""

    schema_version: str = "1.0.0"
    record_type: str = ""
    system_version: str = ""
    experiment_id: str = ""
    timestamp: str = ""
    system_id: str = ""
    measure_id: str = ""
    collector: str = "automated"
    notes: str = ""


@dataclass
class ExperimentRun(CommonEnvelope):
    """A/B test or controlled experiment result."""

    record_type: str = "experiment-run"
    condition_a: dict[str, Any] = field(default_factory=dict)
    condition_b: dict[str, Any] = field(default_factory=dict)
    n: int = 0
    value: float = 0.0
    target: float = 0.0
    comparison: str = "GE"
    passed: bool = False
    confidence_interval: Optional[list[float]] = None
    effect_size: Optional[float] = None
    p_value: Optional[float] = None

    def to_dict(self) -> dict[str, Any]:
        d = {
            "schema_version": self.schema_version,
            "record_type": self.record_type,
            "system_version": self.system_version,
            "experiment_id": self.experiment_id,
            "timestamp": self.timestamp,
            "system_id": self.system_id,
            "measure_id": self.measure_id,
            "collector": self.collector,
            "condition_a": self.condition_a,
            "condition_b": self.condition_b,
            "n": self.n,
            "value": self.value,
            "target": self.target,
            "comparison": self.comparison,
            "pass": self.passed,
        }
        if self.notes:
            d["notes"] = self.notes
        if self.confidence_interval:
            d["confidence_interval"] = self.confidence_interval
        if self.effect_size is not None:
            d["effect_size"] = self.effect_size
        if self.p_value is not None:
            d["p_value"] = self.p_value
        return d


@dataclass
class LongitudinalDataPoint:
    """A single data point in a longitudinal series."""

    system_version: str = ""
    value: float = 0.0
    timestamp: str = ""


@dataclass
class LongitudinalSeries(CommonEnvelope):
    """Time-series tracking of a measure across versions."""

    record_type: str = "longitudinal-series"
    data_points: list[LongitudinalDataPoint] = field(default_factory=list)
    trend_direction: str = "stable"
    trend_slope: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "record_type": self.record_type,
            "system_version": self.system_version,
            "experiment_id": self.experiment_id,
            "timestamp": self.timestamp,
            "system_id": self.system_id,
            "measure_id": self.measure_id,
            "collector": self.collector,
            "data_points": [
                {"system_version": dp.system_version, "value": dp.value,
                 "timestamp": dp.timestamp}
                for dp in self.data_points
            ],
            "trend": {
                "direction": self.trend_direction,
                "slope": self.trend_slope,
            },
            "notes": self.notes,
        }


@dataclass
class PerQueryRecord(CommonEnvelope):
    """Raw per-query data for fine-grained analysis."""

    record_type: str = "per-query-record"
    query: str = ""
    response: str = ""
    signals: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "record_type": self.record_type,
            "system_version": self.system_version,
            "experiment_id": self.experiment_id,
            "timestamp": self.timestamp,
            "system_id": self.system_id,
            "measure_id": self.measure_id,
            "collector": self.collector,
            "query": self.query,
            "response": self.response,
            "signals": self.signals,
            "notes": self.notes,
        }
