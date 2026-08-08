"""Tests for the measure-collection helpers.

The date test below is the one that matters. `record_experiment_run` stamps the
record in UTC and separately builds the output filename from a date. When those
came from two independent clock reads, a run could write a file named for one day
holding a record timestamped the next -- invisible in any timezone whose local
date happens to match UTC, which is why it survived.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone

from acf.measures.collector import record_experiment_run


def _run(tmp_path):
    return record_experiment_run(
        measure_id="M-001",
        experiment_id="EXPR-1",
        system_id="sys",
        system_version="1.0",
        value=0.9,
        target=0.8,
        data_dir=tmp_path,
    )


def test_filename_date_matches_record_timestamp_in_a_skewed_timezone(tmp_path, monkeypatch):
    """The filename's date and the record's own timestamp must never disagree.

    Runs under a deliberately extreme offset so local date and UTC date differ for
    most of the day. Without that, the assertion passes for the wrong reason.
    """
    monkeypatch.setenv("TZ", "Pacific/Midway")  # UTC-11
    if hasattr(time, "tzset"):
        time.tzset()

    record = _run(tmp_path)
    written = list(tmp_path.glob("*.json"))
    assert len(written) == 1, f"expected one record file, got {written}"

    filename_date = written[0].stem.rsplit("_", 1)[-1]
    record_date = record["timestamp"][:10]

    assert filename_date == record_date, (
        f"filename is dated {filename_date} but the record it holds is timestamped "
        f"{record_date} -- the two came from different clock reads"
    )


def test_record_timestamp_is_timezone_aware_utc(tmp_path):
    record = _run(tmp_path)
    parsed = datetime.fromisoformat(record["timestamp"])
    assert parsed.tzinfo is not None, "timestamp must be timezone-aware"
    assert parsed.utcoffset() == timezone.utc.utcoffset(None)


def test_written_file_round_trips(tmp_path):
    record = _run(tmp_path)
    written = list(tmp_path.glob("*.json"))[0]
    assert json.loads(written.read_text()) == record


def test_no_file_written_without_data_dir():
    record = record_experiment_run(
        measure_id="M-001",
        experiment_id="EXPR-1",
        system_id="sys",
        system_version="1.0",
        value=0.9,
        target=0.8,
    )
    assert record["measure_id"] == "M-001"
    assert not any(f.endswith(".json") for f in os.listdir("."))
