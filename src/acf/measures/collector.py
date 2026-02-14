"""Data collection helpers for ACF measures."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def record_experiment_run(
    measure_id: str,
    experiment_id: str,
    system_id: str,
    system_version: str,
    value: float,
    target: float,
    comparison: str = "GE",
    n: int = 0,
    data_dir: Path | None = None,
    notes: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    """Create and optionally save an experiment-run record."""
    now = datetime.now(timezone.utc).isoformat()
    record = {
        "schema_version": "1.0.0",
        "record_type": "experiment-run",
        "system_version": system_version,
        "experiment_id": experiment_id,
        "timestamp": now,
        "system_id": system_id,
        "measure_id": measure_id,
        "collector": kwargs.get("collector", "automated"),
        "n": n,
        "value": value,
        "target": target,
        "comparison": comparison,
        "pass": _evaluate_comparison(value, target, comparison),
        "notes": notes,
    }

    if data_dir:
        data_dir.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{experiment_id}_{measure_id}_{system_id}_{date_str}.json"
        (data_dir / filename).write_text(json.dumps(record, indent=2))

    return record


def _evaluate_comparison(value: float, target: float, comparison: str) -> bool:
    """Evaluate a comparison operation."""
    ops = {
        "GE": value >= target,
        "GT": value > target,
        "LE": value <= target,
        "LT": value < target,
        "EQ": value == target,
    }
    return ops.get(comparison.upper(), False)
