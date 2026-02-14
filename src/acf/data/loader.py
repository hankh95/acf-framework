"""Load ACF data files from directories."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_data_files(data_dir: Path) -> list[dict[str, Any]]:
    """Load all JSON data files from a directory."""
    records = []
    for f in sorted(data_dir.glob("*.json")):
        try:
            records.append(json.loads(f.read_text()))
        except (json.JSONDecodeError, OSError):
            continue
    return records


def load_profiles(profile_dir: Path) -> list[dict[str, Any]]:
    """Load ACF profile JSON files from a directory."""
    from acf.scoring.profile import ACFProfile

    profiles = []
    for f in sorted(profile_dir.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            if "dimensions" in data and "system_id" in data:
                profiles.append(data)
        except (json.JSONDecodeError, OSError):
            continue
    return profiles


def filter_by_measure(records: list[dict], measure_id: str) -> list[dict]:
    """Filter records by measure ID."""
    return [r for r in records if r.get("measure_id") == measure_id]


def filter_by_system(records: list[dict], system_id: str) -> list[dict]:
    """Filter records by system ID."""
    return [
        r for r in records
        if r.get("system_id") == system_id or r.get("being") == system_id
    ]
