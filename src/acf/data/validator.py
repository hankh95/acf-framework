"""Validate ACF data files against expected schemas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


REQUIRED_ENVELOPE_FIELDS = ["record_type", "measure_id"]

VALID_RECORD_TYPES = {"experiment-run", "longitudinal-series", "per-query-record"}

EXPERIMENT_RUN_FIELDS = ["value", "target", "comparison"]
LONGITUDINAL_FIELDS = ["data_points"]


@dataclass
class ValidationResult:
    """Result of validating a data record."""

    valid: bool
    errors: list[str]
    warnings: list[str]
    record_type: str = ""


def validate_record(data: dict[str, Any]) -> ValidationResult:
    """Validate a single data record."""
    errors = []
    warnings = []

    # Check envelope fields
    for field_name in REQUIRED_ENVELOPE_FIELDS:
        if field_name not in data:
            errors.append(f"Missing required field: {field_name}")

    record_type = data.get("record_type", "")
    if record_type and record_type not in VALID_RECORD_TYPES:
        errors.append(f"Invalid record_type: {record_type}")

    # Type-specific validation
    if record_type == "experiment-run":
        for field_name in EXPERIMENT_RUN_FIELDS:
            if field_name not in data:
                warnings.append(f"Missing recommended field: {field_name}")
        if "pass" not in data and "passed" not in data:
            warnings.append("Missing pass/fail indicator")

    elif record_type == "longitudinal-series":
        if "data_points" not in data:
            errors.append("longitudinal-series requires data_points array")
        elif not isinstance(data["data_points"], list):
            errors.append("data_points must be an array")
        elif len(data["data_points"]) == 0:
            warnings.append("data_points array is empty")

    # Optional field warnings
    if "schema_version" not in data:
        warnings.append("Missing schema_version (recommended)")
    if "timestamp" not in data:
        warnings.append("Missing timestamp")
    if "system_id" not in data and "being" not in data:
        warnings.append("Missing system_id (or being)")

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        record_type=record_type,
    )
