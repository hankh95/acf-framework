"""Tests for acf.measures.collector.

`record_experiment_run` had no coverage at all, and a real defect was fixed in it blind: the
record was stamped `datetime.now(timezone.utc)` while the output FILENAME came from a second,
naive `datetime.now()`. For part of every day those disagree, so a run could write a file named
for one date holding a record timestamped another. The suite passed identically with the bug
present, because nothing exercised this module.

WHY THE DATE TEST FREEZES TIME INSTEAD OF SETTING `TZ`.

The obvious way to expose the bug is to run under a skewed zone (say `TZ=Pacific/Midway`,
UTC-11) so the local and UTC dates differ. That works — but only for part of the day. At
UTC-11 the two dates diverge for the 11 hours after UTC midnight and COINCIDE for the other 13.
A test written that way therefore passes for the wrong reason on most runs, and would have gone
green against the broken code more often than red. That is the vacuous-assertion shape, and it
is worse here than no test, because it would be believed.

Freezing both clock reads at a fixed instant that straddles a date boundary makes the assertion
deterministic: it is red against the bug on every run, in every timezone, on every machine,
including CI. The property under test is not "these agree in my timezone" but "the filename
date and the record's timestamp date are derived from the same instant".
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from acf.measures import collector
from acf.measures.collector import _evaluate_comparison, record_experiment_run

# An instant chosen so the naive/local read and the UTC read fall on DIFFERENT dates. This is
# what the bug looked like in production: a file named for one day holding a record stamped
# with the next.
# DTZ001 is suppressed deliberately: a NAIVE local instant is precisely what the buggy code
# read, so making it timezone-aware would remove the thing under test.
LOCAL_INSTANT = datetime(2026, 8, 7, 20, 0, 0)  # noqa: DTZ001
UTC_INSTANT = datetime(2026, 8, 8, 7, 0, 0, tzinfo=timezone.utc)


class _FrozenDateTime(datetime):
    """A `datetime` whose `now()` returns a fixed instant, different per tz argument.

    Subclassing `datetime` rather than using a bare stub keeps `isoformat`/`strftime` real, so
    the test exercises the module's actual formatting rather than a mock's.
    """

    @classmethod
    def now(cls, tz=None):
        return UTC_INSTANT if tz is not None else LOCAL_INSTANT


@pytest.fixture
def frozen_clock(monkeypatch):
    """Freeze both clock reads inside the collector module."""
    monkeypatch.setattr(collector, "datetime", _FrozenDateTime)
    return _FrozenDateTime


def _only_json(directory):
    """Return the single .json in `directory`, asserting there is exactly one.

    Stronger than indexing or `next(iter(...))`: a run that wrote zero or two files is a real
    defect, and this turns it into a clear failure instead of an IndexError or a silent
    first-of-many.
    """
    written = sorted(directory.glob("*.json"))
    assert len(written) == 1, f"expected exactly one json file, got {written}"
    return written[0]


def _run(data_dir=None, **overrides):
    kwargs = {
        "measure_id": "M-1",
        "experiment_id": "EXPR-1",
        "system_id": "sys",
        "system_version": "1.0.0",
        "value": 0.9,
        "target": 0.8,
    }
    kwargs.update(overrides)
    return record_experiment_run(data_dir=data_dir, **kwargs)


class TestFilenameAndTimestampAgree:
    """The regression this module was missing."""

    def test_filename_date_matches_record_timestamp_date(self, frozen_clock, tmp_path):
        """The written file is named for the SAME date the record is stamped with.

        Red against the pre-fix code: the filename came from a naive `datetime.now()` (local)
        while the timestamp came from `datetime.now(timezone.utc)`, so at this instant the file
        would be named `..._2026-08-07.json` while holding a `2026-08-08T07:00:00+00:00` record.
        """
        record = _run(data_dir=tmp_path)

        written = _only_json(tmp_path)
        filename_date = written.stem.rsplit("_", 1)[1]
        timestamp_date = record["timestamp"][:10]

        assert filename_date == timestamp_date, (
            f"filename says {filename_date} but the record it holds is stamped "
            f"{timestamp_date} — the two clock reads disagree"
        )

    def test_both_reads_are_utc(self, frozen_clock, tmp_path):
        """Positively: both derive from the UTC instant, not the local one.

        Stated this way round on purpose. Asserting only that the two AGREE would also be
        satisfied by a version that made both of them naive/local — which would re-introduce
        the same class of bug for anyone whose machine is not on UTC.
        """
        record = _run(data_dir=tmp_path)
        expected = UTC_INSTANT.strftime("%Y-%m-%d")

        assert record["timestamp"] == UTC_INSTANT.isoformat()
        assert _only_json(tmp_path).stem.endswith(expected)


class TestRecordShape:
    def test_record_carries_the_documented_fields(self):
        record = _run(n=42, notes="a note", collector="manual")

        assert record["schema_version"] == "1.0.0"
        assert record["record_type"] == "experiment-run"
        assert record["measure_id"] == "M-1"
        assert record["experiment_id"] == "EXPR-1"
        assert record["system_id"] == "sys"
        assert record["system_version"] == "1.0.0"
        assert record["value"] == 0.9
        assert record["target"] == 0.8
        assert record["comparison"] == "GE"
        assert record["n"] == 42
        assert record["notes"] == "a note"
        assert record["collector"] == "manual"

    def test_collector_defaults_to_automated(self):
        assert _run()["collector"] == "automated"

    def test_pass_is_computed_from_the_comparison(self):
        assert _run(value=0.9, target=0.8, comparison="GE")["pass"] is True
        assert _run(value=0.7, target=0.8, comparison="GE")["pass"] is False


class TestFileWriting:
    def test_no_file_is_written_without_a_data_dir(self, tmp_path):
        """The default is in-memory. A collector that wrote to disk unasked would be a surprise."""
        _run()
        assert list(tmp_path.iterdir()) == []

    def test_the_written_file_round_trips_as_json(self, frozen_clock, tmp_path):
        record = _run(data_dir=tmp_path)
        assert json.loads(_only_json(tmp_path).read_text()) == record

    def test_the_data_dir_is_created_if_absent(self, frozen_clock, tmp_path):
        target = tmp_path / "nested" / "deeper"
        assert not target.exists()
        _run(data_dir=target)
        assert len(list(target.glob("*.json"))) == 1

    def test_the_filename_identifies_the_run(self, frozen_clock, tmp_path):
        _run(data_dir=tmp_path)
        stem = _only_json(tmp_path).stem
        assert stem.startswith("EXPR-1_M-1_sys_")


class TestEvaluateComparison:
    @pytest.mark.parametrize(
        "value,target,comparison,expected",
        [
            (0.9, 0.8, "GE", True),
            (0.8, 0.8, "GE", True),
            (0.7, 0.8, "GE", False),
            (0.9, 0.8, "GT", True),
            (0.8, 0.8, "GT", False),
            (0.7, 0.8, "LE", True),
            (0.8, 0.8, "LE", True),
            (0.9, 0.8, "LE", False),
            (0.7, 0.8, "LT", True),
            (0.8, 0.8, "LT", False),
            (0.8, 0.8, "EQ", True),
            (0.9, 0.8, "EQ", False),
        ],
    )
    def test_each_operator(self, value, target, comparison, expected):
        assert _evaluate_comparison(value, target, comparison) is expected

    def test_comparison_is_case_insensitive(self):
        assert _evaluate_comparison(0.9, 0.8, "ge") is True

    def test_an_unknown_comparison_does_not_pass(self):
        """Fail closed: an operator nobody implemented must not report a pass."""
        assert _evaluate_comparison(0.9, 0.8, "APPROXIMATELY") is False
